#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de datos para el Organizador de Series
Contiene las clases y estructuras de datos principales
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class VideoFile:
    """Representa un archivo de video con sus metadatos"""
    
    def __init__(self, path: str, name: str = None):
        self.path = Path(path)
        self.name = name or self.path.name
        self.size = self._get_file_size()
        self.audio_tracks = []
        self.episode_number = None
        
    def _get_file_size(self) -> str:
        """Obtiene el tamaño del archivo en formato legible"""
        try:
            size_bytes = self.path.stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"
        except:
            return "0 B"
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario"""
        return {
            'path': str(self.path),
            'name': self.name,
            'size': self.size,
            'audio_tracks': self.audio_tracks,
            'episode_number': self.episode_number
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoFile':
        """Crea un objeto desde un diccionario"""
        video_file = cls(data['path'], data.get('name'))
        video_file.size = data.get('size', '0 B')
        video_file.audio_tracks = data.get('audio_tracks', [])
        video_file.episode_number = data.get('episode_number')
        return video_file

class SeriesMetadata:
    """Metadatos de una serie"""
    
    def __init__(self, name: str = "", year: str = "", series_id: str = "", 
                 season: str = "01", start_episode: str = "01"):
        self.name = name
        self.year = year
        self.series_id = series_id
        self.season = season
        self.start_episode = start_episode
        self.tmdb_data = None
        self.jikan_data = None
    
    def generate_series_folder_name(self) -> str:
        """Genera el nombre de la carpeta de la serie"""
        folder_name = self.name
        if self.year:
            folder_name += f" ({self.year})"
        if self.series_id:
            folder_name += f" [tmdbid-{self.series_id}]"
        return folder_name
    
    def generate_season_folder_name(self) -> str:
        """Genera el nombre de la carpeta de temporada"""
        return f"Season {self.season.zfill(2)}"
    
    def generate_episode_name(self, episode_num: int, original_name: str) -> str:
        """Genera el nombre del episodio"""
        # Extraer extensión del archivo original
        original_path = Path(original_name)
        extension = original_path.suffix
        
        # Formato: SeriesName - S01E01 - EpisodeTitle.ext
        episode_name = f"{self.name} - S{self.season.zfill(2)}E{str(episode_num).zfill(2)}"
        
        # Si hay datos de TMDB, agregar título del episodio
        if self.tmdb_data and hasattr(self.tmdb_data, 'episodes'):
            try:
                episode_title = self.tmdb_data.episodes[episode_num - 1].name
                if episode_title:
                    episode_name += f" - {episode_title}"
            except (IndexError, AttributeError):
                pass
        
        return episode_name + extension

class SeriesModel:
    """Modelo principal que maneja la lógica de datos de la aplicación"""
    
    def __init__(self):
        self.video_files: List[VideoFile] = []
        self.metadata = SeriesMetadata()
        self.ffmpeg_path: Optional[str] = None
        self.directory_history: List[str] = []
        self.history_file = Path("organizer_history.json")
        
        self._load_directory_history()
        self._find_ffmpeg()
    
    def _load_directory_history(self):
        """Carga el historial de directorios"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.directory_history = data.get('directories', [])
                    elif isinstance(data, list):
                        self.directory_history = data
                    else:
                        self.directory_history = []
        except Exception as e:
            print(f"Error cargando historial: {e}")
            self.directory_history = []
    
    def save_directory_history(self):
        """Guarda el historial de directorios"""
        try:
            data = {
                'directories': self.directory_history[-10:],  # Mantener solo los últimos 10
                'last_updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def add_to_history(self, directory: str):
        """Añade un directorio al historial"""
        if directory and directory not in self.directory_history:
            self.directory_history.append(directory)
            self.save_directory_history()
    
    def _find_ffmpeg(self):
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
            print(f"Probando ruta: {ffmpeg_path}")
            if ffmpeg_path.exists():
                print(f"FFmpeg encontrado en: {ffmpeg_path}")
                self.ffmpeg_path = str(ffmpeg_path.absolute())
                return
        
        # Buscar en PATH del sistema
        try:
            result = subprocess.run(['where', 'ffmpeg'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.ffmpeg_path = result.stdout.strip().split('\n')[0]
                return
        except:
            pass
        
        self.ffmpeg_path = None
    
    def detect_video_files(self, source_folder: str) -> List[VideoFile]:
        """Detecta archivos de video en una carpeta"""
        if not source_folder or not os.path.exists(source_folder):
            return []
        
        video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        video_files = []
        
        try:
            folder_path = Path(source_folder)
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                    video_file = VideoFile(str(file_path))
                    video_files.append(video_file)
            
            # Ordenar por nombre
            video_files.sort(key=lambda x: x.name.lower())
            
            # Detectar información de audio para archivos MKV
            for video_file in video_files:
                if video_file.path.suffix.lower() == '.mkv':
                    video_file.audio_tracks = self._get_audio_tracks_info(str(video_file.path))
            
            self.video_files = video_files
            self.add_to_history(source_folder)
            
        except Exception as e:
            print(f"Error detectando archivos: {e}")
        
        return self.video_files
    
    def _get_audio_tracks_info(self, file_path: str) -> List[Dict]:
        """Obtiene información de las pistas de audio de un archivo"""
        if not self.ffmpeg_path:
            return []
        
        try:
            cmd = [
                self.ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe'),
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-select_streams', 'a',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                audio_tracks = []
                
                for i, stream in enumerate(data.get('streams', [])):
                    track_info = {
                        'index': i,
                        'codec': stream.get('codec_name', 'unknown'),
                        'language': stream.get('tags', {}).get('language', 'und'),
                        'title': stream.get('tags', {}).get('title', f'Audio {i+1}'),
                        'channels': stream.get('channels', 0),
                        'sample_rate': stream.get('sample_rate', 0)
                    }
                    audio_tracks.append(track_info)
                
                return audio_tracks
        
        except Exception as e:
            print(f"Error obteniendo info de audio: {e}")
        
        return []
    
    def move_file_up(self, index: int) -> bool:
        """Mueve un archivo hacia arriba en la lista"""
        if index <= 0 or index >= len(self.video_files):
            return False
        
        self.video_files[index], self.video_files[index-1] = \
            self.video_files[index-1], self.video_files[index]
        return True
    
    def move_file_down(self, index: int) -> bool:
        """Mueve un archivo hacia abajo en la lista"""
        if index < 0 or index >= len(self.video_files) - 1:
            return False
        
        self.video_files[index], self.video_files[index+1] = \
            self.video_files[index+1], self.video_files[index]
        return True
    
    def move_file_to_position(self, from_index: int, to_position: int) -> bool:
        """Mueve un archivo a una posición específica"""
        if (from_index < 0 or from_index >= len(self.video_files) or 
            to_position < 1 or to_position > len(self.video_files)):
            return False
        
        file_to_move = self.video_files.pop(from_index)
        self.video_files.insert(to_position - 1, file_to_move)
        return True
    
    def remove_file(self, index: int) -> bool:
        """Elimina un archivo de la lista"""
        if index < 0 or index >= len(self.video_files):
            return False
        
        del self.video_files[index]
        return True
    
    def get_episode_number(self, file_index: int) -> int:
        """Calcula el número de episodio para un archivo"""
        try:
            start_ep = int(self.metadata.start_episode)
            return start_ep + file_index
        except ValueError:
            return file_index + 1
    
    def update_start_episode_from_file(self, file_index: int, new_episode: int):
        """Actualiza el episodio inicial basado en un archivo específico"""
        new_start = new_episode - file_index
        self.metadata.start_episode = str(new_start)