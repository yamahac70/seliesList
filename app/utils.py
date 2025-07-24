#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades y funciones auxiliares para el Organizador de Series
"""

import subprocess
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    from tmdbv3api import TMDb, TV
    TMDB_AVAILABLE = True
except ImportError:
    TMDB_AVAILABLE = False
    TMDb = None
    TV = None

try:
    from jikan_api import JikanAPI, AnimeResult
    JIKAN_AVAILABLE = True
except ImportError:
    JIKAN_AVAILABLE = False
    JikanAPI = None
    AnimeResult = None

class FFmpegProcessor:
    """Procesador de video usando FFmpeg"""
    
    def __init__(self, ffmpeg_path: str = None):
        self.ffmpeg_path = ffmpeg_path or self._find_ffmpeg()
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Busca FFmpeg en el sistema"""
        # Lista de rutas locales donde buscar FFmpeg
        local_paths = [
            Path("bin/ffmpeg.exe"),
            Path("ffmpeg/bin/ffmpeg.exe"),
            Path("../bin/ffmpeg.exe"),
            Path("../ffmpeg/bin/ffmpeg.exe"),
            Path("util/ffmpeg.exe"),
            Path("utils/ffmpeg.exe"),
            Path("tools/ffmpeg.exe"),
            Path("ffmpeg.exe")
        ]
        
        # Buscar en las carpetas locales primero
        for ffmpeg_path in local_paths:
            if ffmpeg_path.exists():
                return str(ffmpeg_path.absolute())
        
        # Buscar en PATH del sistema
        try:
            result = subprocess.run(['where', 'ffmpeg'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return None
    
    def is_available(self) -> bool:
        """Verifica si FFmpeg está disponible"""
        return self.ffmpeg_path is not None
    
    def get_video_info(self, file_path: str) -> Dict:
        """Obtiene información del video"""
        if not self.ffmpeg_path:
            return {}
        
        try:
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
            cmd = [
                ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        
        except Exception as e:
            print(f"Error obteniendo info del video: {e}")
        
        return {}
    
    def get_audio_tracks(self, file_path: str) -> List[Dict]:
        """Obtiene información de las pistas de audio"""
        video_info = self.get_video_info(file_path)
        audio_tracks = []
        
        for i, stream in enumerate(video_info.get('streams', [])):
            if stream.get('codec_type') == 'audio':
                track_info = {
                    'index': i,
                    'codec': stream.get('codec_name', 'unknown'),
                    'language': stream.get('tags', {}).get('language', 'und'),
                    'title': stream.get('tags', {}).get('title', f'Audio {len(audio_tracks)+1}'),
                    'channels': stream.get('channels', 0),
                    'sample_rate': stream.get('sample_rate', 0)
                }
                audio_tracks.append(track_info)
        
        return audio_tracks
    
    def convert_video(self, input_path: str, output_path: str, resolution: str = "Original",
                     compression_level: str = "Medium", audio_mode: str = "keep_all",
                     selected_audio_track: str = "0") -> bool:
        """Convierte un archivo de video con manejo mejorado de errores y progreso en tiempo real"""
        if not self.ffmpeg_path:
            print("❌ FFmpeg no está disponible")
            return False
        
        # Validar entrada (archivo local o URL)
        is_url = input_path.startswith(('http://', 'https://', 'ftp://'))
        
        if not is_url:
            # Validar archivo local
            input_file = Path(input_path)
            if not input_file.exists():
                print(f"❌ Archivo de entrada no existe: {input_path}")
                return False
            
            if not input_file.is_file():
                print(f"❌ La ruta no es un archivo válido: {input_path}")
                return False
        else:
            print(f"🌐 Procesando URL: {input_path[:80]}...")
        
        # Crear directorio de salida si no existe
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            cmd = [self.ffmpeg_path, '-i', input_path, '-progress', 'pipe:1']
            
            # Configurar resolución
            if resolution != "Original":
                if resolution == "1080p":
                    cmd.extend(['-vf', 'scale=1920:1080'])
                elif resolution == "720p":
                    cmd.extend(['-vf', 'scale=1280:720'])
                elif resolution == "480p":
                    cmd.extend(['-vf', 'scale=854:480'])
            
            # Configurar compresión
            if compression_level == "High":
                cmd.extend(['-crf', '18'])
            elif compression_level == "Medium":
                cmd.extend(['-crf', '23'])
            elif compression_level == "Low":
                cmd.extend(['-crf', '28'])
            
            # Configurar audio con validación
            if audio_mode == "select_track":
                # Verificar que la pista de audio existe
                audio_tracks = self.get_audio_tracks(input_path)
                track_index = int(selected_audio_track)
                
                if not audio_tracks:
                    print("⚠️ No se encontraron pistas de audio, usando configuración por defecto")
                    cmd.extend(['-c:a', 'copy'])
                elif track_index >= len(audio_tracks):
                    print(f"⚠️ Pista de audio {track_index} no existe, usando pista 0")
                    cmd.extend(['-map', '0:v', '-map', '0:a:0'])
                else:
                    cmd.extend(['-map', '0:v', '-map', f'0:a:{selected_audio_track}'])
            elif audio_mode == "keep_all":
                cmd.extend(['-c:a', 'copy'])
            
            # Configurar codec de video
            cmd.extend(['-c:v', 'libx264', '-preset', 'medium'])
            
            # Archivo de salida
            cmd.extend(['-y', output_path])
            
            if is_url:
                print(f"🔄 Iniciando conversión desde URL")
            else:
                print(f"🔄 Iniciando conversión: {input_file.name}")
            print(f"📝 Comando: {' '.join(cmd[:3])} ... [parámetros de conversión]")
            
            # Ejecutar conversión con progreso en tiempo real
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     text=True, universal_newlines=True)
            
            # Monitorear progreso
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    if line.startswith('frame='):
                        # Extraer información de progreso
                        parts = line.split()
                        frame_info = {}
                        for part in parts:
                            if '=' in part:
                                key, value = part.split('=', 1)
                                frame_info[key] = value
                        
                        if 'frame' in frame_info and 'time' in frame_info:
                            print(f"⏳ Progreso: frame {frame_info['frame']}, tiempo {frame_info['time']}")
            
            # Esperar a que termine el proceso
            return_code = process.wait()
            
            if return_code == 0:
                print(f"✅ Conversión exitosa: {output_file.name}")
                return True
            else:
                stderr_output = process.stderr.read()
                print(f"❌ Error en conversión (código {return_code})")
                if stderr_output:
                    print(f"📋 Error FFmpeg: {stderr_output[-500:]}")  # Últimos 500 caracteres
                return False
            
        except Exception as e:
            print(f"❌ Error inesperado convirtiendo video: {e}")
            return False
    
    def extract_audio(self, input_path: str, output_path: str, 
                     audio_format: str = "mp3", selected_track: str = "0") -> bool:
        """Extrae audio de un archivo de video con manejo mejorado de errores y progreso en tiempo real"""
        if not self.ffmpeg_path:
            print("❌ FFmpeg no está disponible")
            return False
        
        # Validar archivo de entrada
        input_file = Path(input_path)
        if not input_file.exists():
            print(f"❌ Archivo de entrada no existe: {input_path}")
            return False
        
        if not input_file.is_file():
            print(f"❌ La ruta no es un archivo válido: {input_path}")
            return False
        
        # Crear directorio de salida si no existe
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Verificar que la pista de audio existe
            audio_tracks = self.get_audio_tracks(input_path)
            track_index = int(selected_track)
            
            if not audio_tracks:
                print("❌ No se encontraron pistas de audio en el archivo")
                return False
            
            if track_index >= len(audio_tracks):
                print(f"⚠️ Pista de audio {track_index} no existe, usando pista 0")
                selected_track = "0"
            
            # Configurar codec según formato
            if audio_format == 'mp3':
                audio_codec = 'libmp3lame'
            elif audio_format == 'aac':
                audio_codec = 'aac'
            elif audio_format == 'wav':
                audio_codec = 'pcm_s16le'
            else:
                audio_codec = 'libmp3lame'  # Por defecto MP3
            
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-progress', 'pipe:1',
                '-map', f'0:a:{selected_track}',
                '-vn',  # Sin video
                '-acodec', audio_codec,
                '-y', output_path
            ]
            
            print(f"🎵 Iniciando extracción de audio: {input_file.name}")
            print(f"📝 Formato: {audio_format.upper()}, Pista: {selected_track}")
            
            # Ejecutar extracción con progreso en tiempo real
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     text=True, universal_newlines=True)
            
            # Monitorear progreso
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    if line.startswith('size='):
                        # Extraer información de progreso para audio
                        parts = line.split()
                        progress_info = {}
                        for part in parts:
                            if '=' in part:
                                key, value = part.split('=', 1)
                                progress_info[key] = value
                        
                        if 'size' in progress_info and 'time' in progress_info:
                            print(f"⏳ Progreso: tamaño {progress_info['size']}, tiempo {progress_info['time']}")
            
            # Esperar a que termine el proceso
            return_code = process.wait()
            
            if return_code == 0:
                print(f"✅ Audio extraído exitosamente: {output_file.name}")
                return True
            else:
                stderr_output = process.stderr.read()
                print(f"❌ Error en extracción de audio (código {return_code})")
                if stderr_output:
                    print(f"📋 Error FFmpeg: {stderr_output[-500:]}")  # Últimos 500 caracteres
                return False
            
        except Exception as e:
            print(f"❌ Error inesperado extrayendo audio: {e}")
            return False

class MetadataSearcher:
    """Buscador de metadatos de series"""
    
    def __init__(self):
        self.tmdb = None
        self.jikan = None
        
        if TMDB_AVAILABLE:
            try:
                self.tmdb = TMDb()
                # Aquí deberías configurar tu API key de TMDB
                # self.tmdb.api_key = 'tu_api_key_aqui'
            except:
                pass
        
        if JIKAN_AVAILABLE:
            try:
                self.jikan = JikanAPI()
            except:
                pass
    
    def search_tmdb(self, query: str) -> List[Dict]:
        """Busca series en TMDB"""
        if not self.tmdb or not TMDB_AVAILABLE:
            return []
        
        try:
            tv = TV()
            results = tv.search(query)
            
            formatted_results = []
            for result in results[:10]:  # Limitar a 10 resultados
                formatted_result = {
                    'id': result.id,
                    'name': result.name,
                    'original_name': result.original_name,
                    'overview': result.overview,
                    'first_air_date': result.first_air_date,
                    'vote_average': result.vote_average,
                    'poster_path': result.poster_path
                }
                formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error buscando en TMDB: {e}")
            return []
    
    def search_jikan(self, query: str) -> List[Dict]:
        """Busca anime en Jikan (MyAnimeList)"""
        if not self.jikan or not JIKAN_AVAILABLE:
            return []
        
        try:
            results = self.jikan.search_anime(query, limit=10)
            
            formatted_results = []
            for result in results:
                formatted_result = {
                    'id': result.mal_id,
                    'title': result.title,
                    'title_english': result.title_english,
                    'synopsis': result.synopsis,
                    'year': result.year,
                    'score': result.score,
                    'episodes': result.episodes,
                    'status': result.status,
                    'image_url': result.image_url
                }
                formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error buscando en Jikan: {e}")
            return []
    
    def get_tmdb_details(self, series_id: int) -> Optional[Dict]:
        """Obtiene detalles completos de una serie de TMDB"""
        if not self.tmdb or not TMDB_AVAILABLE:
            return None
        
        try:
            tv = TV()
            details = tv.details(series_id)
            return details.__dict__
        except Exception as e:
            print(f"Error obteniendo detalles de TMDB: {e}")
            return None
    
    def get_jikan_details(self, anime_id: int) -> Optional[Dict]:
        """Obtiene detalles completos de un anime de Jikan"""
        if not self.jikan or not JIKAN_AVAILABLE:
            return None
        
        try:
            details = self.jikan.get_anime_details(anime_id)
            return details.__dict__ if details else None
        except Exception as e:
            print(f"Error obteniendo detalles de Jikan: {e}")
            return None

class FileUtils:
    """Utilidades para manejo de archivos"""
    
    @staticmethod
    def get_file_size_formatted(file_path: str) -> str:
        """Obtiene el tamaño del archivo en formato legible"""
        try:
            size_bytes = Path(file_path).stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"
        except:
            return "0 B"
    
    @staticmethod
    def is_video_file(file_path: str) -> bool:
        """Verifica si un archivo es de video"""
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        return Path(file_path).suffix.lower() in video_extensions
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitiza un nombre de archivo eliminando caracteres no válidos"""
        import re
        # Eliminar caracteres no válidos para nombres de archivo
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Reemplazar múltiples espacios con uno solo
        sanitized = re.sub(r'\s+', ' ', sanitized)
        return sanitized.strip()
    
    @staticmethod
    def extract_episode_number(filename: str) -> Optional[int]:
        """Intenta extraer el número de episodio del nombre del archivo"""
        import re
        
        # Patrones comunes para números de episodio
        patterns = [
            r'[Ee]pisode[\s_]*([0-9]+)',
            r'[Ee]p[\s_]*([0-9]+)',
            r'[\s_-]([0-9]+)[\s_-]',
            r'^([0-9]+)[\s_-]',
            r'[\s_-]([0-9]+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return None

class ConfigManager:
    """Gestor de configuración de la aplicación"""
    
    def __init__(self, config_file: str = "data/config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Carga la configuración desde archivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
        
        # Configuración por defecto
        return {
            'theme': 'dark',
            'default_resolution': 'Original',
            'default_compression': 'Medium',
            'jellyfin_structure': True,
            'create_nfo': False,
            'tmdb_api_key': '',
            'last_directories': []
        }
    
    def save_config(self):
        """Guarda la configuración a archivo"""
        try:
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def get(self, key: str, default=None):
        """Obtiene un valor de configuración"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Establece un valor de configuración"""
        self.config[key] = value
        self.save_config()
    
    def update(self, updates: Dict):
        """Actualiza múltiples valores de configuración"""
        self.config.update(updates)
        self.save_config()