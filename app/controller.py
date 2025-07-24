#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlador para el Organizador de Series
Maneja la lógica de control entre la vista y el modelo
"""

import threading
import subprocess
import shutil
from pathlib import Path
from typing import Callable, Optional, List, Dict
from .model import SeriesModel, VideoFile, SeriesMetadata
from .utils import FFmpegProcessor, MetadataSearcher

class SeriesController:
    """Controlador principal de la aplicación"""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.model = SeriesModel()
        self.ffmpeg_processor = FFmpegProcessor()
        self.metadata_searcher = MetadataSearcher()
        
        # Callbacks para la vista
        self.on_files_updated: Optional[Callable] = None
        self.on_progress_updated: Optional[Callable] = None
        self.on_log_message: Optional[Callable] = None
        self.on_processing_started: Optional[Callable] = None
        self.on_processing_finished: Optional[Callable] = None
        
        # Estado del procesamiento
        self.is_processing = False
        self.current_file = 0
        self.total_files = 0
        self.stop_processing = False
    
    def set_callbacks(self, **callbacks):
        """Establece los callbacks para comunicación con la vista"""
        for name, callback in callbacks.items():
            if hasattr(self, f'on_{name}'):
                setattr(self, f'on_{name}', callback)
    
    def log_message(self, message: str):
        """Envía un mensaje al log"""
        if self.on_log_message:
            self.on_log_message(message)
    
    def update_progress(self, current: int, total: int, message: str = ""):
        """Actualiza el progreso"""
        if self.on_progress_updated:
            self.on_progress_updated(current, total, message)
    
    def notify_files_updated(self):
        """Notifica que la lista de archivos se actualizó"""
        if self.on_files_updated:
            self.on_files_updated()
    
    # Métodos de gestión de archivos
    def detect_video_files(self, source_folder: str) -> bool:
        """Detecta archivos de video en una carpeta"""
        try:
            files = self.model.detect_video_files(source_folder)
            self.log_message(f"📁 Detectados {len(files)} archivos de video en: {source_folder}")
            self.notify_files_updated()
            return True
        except Exception as e:
            self.log_message(f"❌ Error detectando archivos: {str(e)}")
            return False
    
    def move_file_up(self, index: int) -> bool:
        """Mueve un archivo hacia arriba"""
        if self.model.move_file_up(index):
            self.log_message(f"⬆️ Archivo movido hacia arriba: {self.model.video_files[index-1].name}")
            self.notify_files_updated()
            return True
        return False
    
    def move_file_down(self, index: int) -> bool:
        """Mueve un archivo hacia abajo"""
        if self.model.move_file_down(index):
            self.log_message(f"⬇️ Archivo movido hacia abajo: {self.model.video_files[index+1].name}")
            self.notify_files_updated()
            return True
        return False
    
    def move_file_to_position(self, from_index: int, to_position: int) -> bool:
        """Mueve un archivo a una posición específica"""
        if from_index < 0 or from_index >= len(self.model.video_files):
            return False
        
        file_name = self.model.video_files[from_index].name
        if self.model.move_file_to_position(from_index, to_position):
            self.log_message(f"📝 Archivo reposicionado: {file_name} movido a posición {to_position}")
            self.notify_files_updated()
            return True
        return False
    
    def remove_file(self, index: int) -> bool:
        """Elimina un archivo de la lista"""
        if index < 0 or index >= len(self.model.video_files):
            return False
        
        file_name = self.model.video_files[index].name
        if self.model.remove_file(index):
            self.log_message(f"🗑️ Archivo quitado de la lista: {file_name}")
            self.notify_files_updated()
            return True
        return False
    
    def update_episode_number(self, file_index: int, new_episode: int) -> bool:
        """Actualiza el número de episodio para un archivo específico"""
        try:
            self.model.update_start_episode_from_file(file_index, new_episode)
            self.log_message(f"📝 Episodio actualizado: Archivo {file_index + 1} ahora es episodio {new_episode}")
            self.notify_files_updated()
            return True
        except Exception as e:
            self.log_message(f"❌ Error actualizando episodio: {str(e)}")
            return False
    
    # Métodos de metadatos
    def update_series_metadata(self, name: str = None, year: str = None, 
                             series_id: str = None, season: str = None, 
                             start_episode: str = None):
        """Actualiza los metadatos de la serie"""
        if name is not None:
            self.model.metadata.name = name
        if year is not None:
            self.model.metadata.year = year
        if series_id is not None:
            self.model.metadata.series_id = series_id
        if season is not None:
            self.model.metadata.season = season
        if start_episode is not None:
            self.model.metadata.start_episode = start_episode
    
    def search_metadata(self, query: str, source: str = "tmdb") -> List[Dict]:
        """Busca metadatos de la serie"""
        try:
            if source == "tmdb":
                results = self.metadata_searcher.search_tmdb(query)
            elif source == "jikan":
                results = self.metadata_searcher.search_jikan(query)
            else:
                return []
            
            self.log_message(f"🔍 Encontrados {len(results)} resultados para '{query}' en {source.upper()}")
            return results
        except Exception as e:
            self.log_message(f"❌ Error buscando metadatos: {str(e)}")
            return []
    
    def apply_metadata(self, metadata: Dict, source: str = "tmdb"):
        """Aplica metadatos seleccionados a la serie"""
        try:
            if source == "tmdb":
                self.model.metadata.name = metadata.get('name', '')
                self.model.metadata.year = str(metadata.get('first_air_date', '')[:4]) if metadata.get('first_air_date') else ''
                self.model.metadata.series_id = str(metadata.get('id', ''))
                self.model.metadata.tmdb_data = metadata
            elif source == "jikan":
                self.model.metadata.name = metadata.get('title', '')
                self.model.metadata.year = str(metadata.get('year', '')) if metadata.get('year') else ''
                self.model.metadata.jikan_data = metadata
            
            self.log_message(f"✅ Metadatos aplicados desde {source.upper()}: {self.model.metadata.name}")
        except Exception as e:
            self.log_message(f"❌ Error aplicando metadatos: {str(e)}")
    
    # Métodos de procesamiento
    def start_processing(self, operation_mode: str, output_directory: str, 
                        resolution: str = "Original", compression_level: str = "Medium",
                        audio_mode: str = "keep_all", selected_audio_track: str = "0",
                        audio_format: str = "mp3", jellyfin_structure: bool = True,
                        create_nfo: bool = False) -> bool:
        """Inicia el procesamiento de archivos"""
        
        # Validaciones
        if not self.model.video_files:
            self.log_message("⚠️ No hay archivos para procesar")
            return False
        
        if not self.model.metadata.name.strip():
            self.log_message("⚠️ Ingresa el nombre de la serie")
            return False
        
        if not output_directory:
            self.log_message("⚠️ Selecciona una carpeta destino")
            return False
        
        if operation_mode in ["convert", "extract_audio"] and not self.model.ffmpeg_path:
            self.log_message("❌ FFmpeg no está disponible. No se puede convertir o extraer audio")
            return False
        
        # Configurar procesamiento
        self.is_processing = True
        self.stop_processing = False
        self.current_file = 0
        self.total_files = len(self.model.video_files)
        
        if self.on_processing_started:
            self.on_processing_started()
        
        # Iniciar en hilo separado
        processing_thread = threading.Thread(
            target=self._process_files,
            args=(operation_mode, output_directory, resolution, compression_level,
                  audio_mode, selected_audio_track, audio_format, 
                  jellyfin_structure, create_nfo),
            daemon=True
        )
        processing_thread.start()
        
        return True
    
    def stop_processing_request(self):
        """Solicita detener el procesamiento"""
        self.stop_processing = True
        self.log_message("🛑 Solicitando detener procesamiento...")
    
    def _process_files(self, operation_mode: str, output_directory: str,
                      resolution: str, compression_level: str, audio_mode: str,
                      selected_audio_track: str, audio_format: str,
                      jellyfin_structure: bool, create_nfo: bool):
        """Procesa todos los archivos (ejecutado en hilo separado)"""
        try:
            # Crear directorio de trabajo
            work_dir = self._create_work_directory(output_directory, jellyfin_structure)
            
            # Informar al usuario dónde se guardarán los archivos
            self.log_message(f"📁 Directorio de salida: {work_dir}")
            self.log_message(f"🎯 Modo de operación: {operation_mode}")
            
            # Procesar cada archivo
            for i, video_file in enumerate(self.model.video_files):
                if self.stop_processing:
                    break
                
                self.current_file = i + 1
                episode_num = self.model.get_episode_number(i)
                
                self.update_progress(self.current_file, self.total_files, 
                                   f"Procesando: {video_file.name}")
                
                success = self._process_single_file(
                    video_file, work_dir, episode_num, operation_mode,
                    resolution, compression_level, audio_mode,
                    selected_audio_track, audio_format
                )
                
                if not success and not self.stop_processing:
                    self.log_message(f"❌ Error procesando: {video_file.name}")
            
            # Crear archivos NFO si está habilitado
            if create_nfo and not self.stop_processing:
                self._create_nfo_files(work_dir)
            
            # Mostrar resumen final
            if not self.stop_processing:
                self.log_message(f"📂 Archivos guardados en: {work_dir}")
                self.log_message(f"📊 Total procesados: {self.current_file}/{self.total_files}")
            
        except Exception as e:
            self.log_message(f"❌ Error durante el procesamiento: {str(e)}")
        
        finally:
            self.is_processing = False
            if self.on_processing_finished:
                self.on_processing_finished()
            
            if self.stop_processing:
                self.log_message("🛑 Procesamiento detenido por el usuario")
            else:
                self.log_message("🎉 ¡Conversión completada!")
    
    def _create_work_directory(self, output_directory: str, jellyfin_structure: bool) -> Path:
        """Crea el directorio de trabajo"""
        output_path = Path(output_directory)
        
        if jellyfin_structure:
            # Estructura Jellyfin: Series Name [year] [id]/Season XX/
            series_folder_name = self.model.metadata.generate_series_folder_name()
            series_dir = output_path / series_folder_name
            series_dir.mkdir(exist_ok=True)
            
            season_folder_name = self.model.metadata.generate_season_folder_name()
            work_dir = series_dir / season_folder_name
            work_dir.mkdir(exist_ok=True)
        else:
            # Estructura simple
            work_dir = output_path / self.model.metadata.name
            work_dir.mkdir(exist_ok=True)
        
        return work_dir
    
    def _process_single_file(self, video_file: VideoFile, work_dir: Path, 
                           episode_num: int, operation_mode: str, resolution: str,
                           compression_level: str, audio_mode: str,
                           selected_audio_track: str, audio_format: str) -> bool:
        """Procesa un archivo individual"""
        try:
            # Generar nombre de salida
            output_name = self.model.metadata.generate_episode_name(episode_num, video_file.name)
            output_path = work_dir / output_name
            
            if operation_mode == "rename":
                # Solo copiar/renombrar
                self.log_message(f"📋 Copiando: {video_file.name} → {output_name}")
                shutil.copy2(video_file.path, output_path)
                self.log_message(f"✅ Copiado: {output_name} → {output_path}")
                
            elif operation_mode == "convert":
                # Convertir con FFmpeg
                self.log_message(f"🎬 Convirtiendo: {video_file.name} → {output_name}")
                self.log_message(f"⚙️ Configuración: {resolution}, compresión {compression_level}, audio {audio_mode}")
                
                success = self.ffmpeg_processor.convert_video(
                    str(video_file.path), str(output_path), resolution,
                    compression_level, audio_mode, selected_audio_track
                )
                if success:
                    self.log_message(f"✅ Convertido: {output_name} → {output_path}")
                else:
                    self.log_message(f"❌ Error convirtiendo: {output_name}")
                    return False
                    
            elif operation_mode == "extract_audio":
                # Extraer audio
                audio_output = output_path.with_suffix(f'.{audio_format}')
                self.log_message(f"🎵 Extrayendo audio: {video_file.name} → {audio_output.name}")
                self.log_message(f"⚙️ Formato: {audio_format}, pista {selected_audio_track}")
                
                success = self.ffmpeg_processor.extract_audio(
                    str(video_file.path), str(audio_output), audio_format,
                    selected_audio_track
                )
                if success:
                    self.log_message(f"✅ Audio extraído: {audio_output.name} → {audio_output}")
                else:
                    self.log_message(f"❌ Error extrayendo audio: {audio_output.name}")
                    return False
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error procesando {video_file.name}: {str(e)}")
            return False
    
    def _create_nfo_files(self, work_dir: Path):
        """Crea archivos NFO para Jellyfin/Kodi"""
        try:
            # Crear tvshow.nfo para la serie
            if self.model.metadata.tmdb_data:
                nfo_content = self._generate_tvshow_nfo()
                nfo_path = work_dir.parent / "tvshow.nfo"
                with open(nfo_path, 'w', encoding='utf-8') as f:
                    f.write(nfo_content)
                self.log_message("📄 Archivo tvshow.nfo creado")
        except Exception as e:
            self.log_message(f"❌ Error creando archivos NFO: {str(e)}")
    
    def _generate_tvshow_nfo(self) -> str:
        """Genera contenido NFO para la serie"""
        tmdb_data = self.model.metadata.tmdb_data
        if not tmdb_data:
            return ""
        
        nfo_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<tvshow>
    <title>{tmdb_data.get('name', '')}</title>
    <originaltitle>{tmdb_data.get('original_name', '')}</originaltitle>
    <showtitle>{tmdb_data.get('name', '')}</showtitle>
    <plot>{tmdb_data.get('overview', '')}</plot>
    <year>{tmdb_data.get('first_air_date', '')[:4] if tmdb_data.get('first_air_date') else ''}</year>
    <premiered>{tmdb_data.get('first_air_date', '')}</premiered>
    <status>{tmdb_data.get('status', '')}</status>
    <tmdbid>{tmdb_data.get('id', '')}</tmdbid>
    <rating>{tmdb_data.get('vote_average', 0)}</rating>
    <votes>{tmdb_data.get('vote_count', 0)}</votes>
</tvshow>"""
        
        return nfo_content
    
    # Propiedades de acceso al modelo
    @property
    def video_files(self) -> List[VideoFile]:
        return self.model.video_files
    
    @property
    def metadata(self) -> SeriesMetadata:
        return self.model.metadata
    
    @property
    def ffmpeg_available(self) -> bool:
        return self.model.ffmpeg_path is not None
    
    @property
    def directory_history(self) -> List[str]:
        return self.model.directory_history