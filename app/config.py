#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Configuración para el Organizador de Series
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Gestor de configuración de la aplicación"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_default_config()
        self.load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Cargar configuración por defecto"""
        return {
            "app": {
                "theme": "dark",
                "color_theme": "blue",
                "window_size": "1200x900",
                "auto_save": True,
                "language": "es"
            },
            "paths": {
                "last_source_folder": "",
                "last_output_folder": "",
                "ffmpeg_path": "",
                "temp_folder": "temp"
            },
            "series": {
                "default_season": 1,
                "default_start_episode": 1,
                "jellyfin_structure": True,
                "create_nfo": True,
                "auto_detect_episode": True
            },
            "processing": {
                "default_operation": "rename",
                "default_resolution": "Original",
                "default_compression": "Medium",
                "default_audio_mode": "keep_all",
                "default_audio_format": "mp3",
                "max_concurrent_processes": 2,
                "backup_original": False
            },
            "metadata": {
                "default_search_source": "tmdb",
                "tmdb_api_key": "",
                "auto_search": False,
                "cache_metadata": True,
                "cache_duration_days": 7
            },
            "ui": {
                "show_file_sizes": True,
                "show_progress_details": True,
                "auto_scroll_log": True,
                "confirm_operations": True,
                "remember_window_position": True
            },
            "advanced": {
                "debug_mode": False,
                "log_level": "INFO",
                "max_log_size_mb": 10,
                "enable_telemetry": False
            }
        }
    
    def load_config(self) -> bool:
        """Cargar configuración desde archivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Fusionar con configuración por defecto
                    self._merge_config(self.config, loaded_config)
                return True
        except Exception as e:
            print(f"Error cargando configuración: {e}")
        return False
    
    def save_config(self) -> bool:
        """Guardar configuración a archivo"""
        try:
            # Crear directorio si no existe
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def _merge_config(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> None:
        """Fusionar configuración cargada con la por defecto"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
    
    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """Obtener valor de configuración"""
        try:
            if key is None:
                return self.config.get(section, default)
            return self.config.get(section, {}).get(key, default)
        except Exception:
            return default
    
    def set(self, section: str, key: str = None, value: Any = None) -> None:
        """Establecer valor de configuración"""
        try:
            if key is None and isinstance(section, str) and value is not None:
                # Formato: set("section.key", value)
                parts = section.split('.', 1)
                if len(parts) == 2:
                    section, key = parts
                    value = value
            
            if section not in self.config:
                self.config[section] = {}
            
            if key is None:
                if isinstance(value, dict):
                    self.config[section] = value
            else:
                self.config[section][key] = value
                
            # Auto-guardar si está habilitado
            if self.get("app", "auto_save", True):
                self.save_config()
        except Exception as e:
            print(f"Error estableciendo configuración: {e}")
    
    def get_app_config(self) -> Dict[str, Any]:
        """Obtener configuración de la aplicación"""
        return self.get("app", default={})
    
    def get_paths_config(self) -> Dict[str, Any]:
        """Obtener configuración de rutas"""
        return self.get("paths", default={})
    
    def get_series_config(self) -> Dict[str, Any]:
        """Obtener configuración de series"""
        return self.get("series", default={})
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Obtener configuración de procesamiento"""
        return self.get("processing", default={})
    
    def get_metadata_config(self) -> Dict[str, Any]:
        """Obtener configuración de metadatos"""
        return self.get("metadata", default={})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Obtener configuración de UI"""
        return self.get("ui", default={})
    
    def get_advanced_config(self) -> Dict[str, Any]:
        """Obtener configuración avanzada"""
        return self.get("advanced", default={})
    
    def update_last_folders(self, source_folder: str = None, output_folder: str = None) -> None:
        """Actualizar últimas carpetas utilizadas"""
        if source_folder:
            self.set("paths", "last_source_folder", source_folder)
        if output_folder:
            self.set("paths", "last_output_folder", output_folder)
    
    def get_last_folders(self) -> tuple[str, str]:
        """Obtener últimas carpetas utilizadas"""
        source = self.get("paths", "last_source_folder", "")
        output = self.get("paths", "last_output_folder", "")
        return source, output
    
    def set_ffmpeg_path(self, path: str) -> None:
        """Establecer ruta de FFmpeg"""
        self.set("paths", "ffmpeg_path", path)
    
    def get_ffmpeg_path(self) -> str:
        """Obtener ruta de FFmpeg"""
        return self.get("paths", "ffmpeg_path", "")
    
    def get_temp_folder(self) -> str:
        """Obtener carpeta temporal"""
        temp_folder = self.get("paths", "temp_folder", "temp")
        # Crear carpeta si no existe
        Path(temp_folder).mkdir(parents=True, exist_ok=True)
        return temp_folder
    
    def is_debug_mode(self) -> bool:
        """Verificar si está en modo debug"""
        return self.get("advanced", "debug_mode", False)
    
    def get_log_level(self) -> str:
        """Obtener nivel de log"""
        return self.get("advanced", "log_level", "INFO")
    
    def reset_to_defaults(self) -> None:
        """Resetear configuración a valores por defecto"""
        self.config = self._load_default_config()
        self.save_config()
    
    def export_config(self, file_path: str) -> bool:
        """Exportar configuración a archivo"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exportando configuración: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Importar configuración desde archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                # Validar estructura básica
                if isinstance(imported_config, dict):
                    self.config = self._load_default_config()
                    self._merge_config(self.config, imported_config)
                    self.save_config()
                    return True
        except Exception as e:
            print(f"Error importando configuración: {e}")
        return False
    
    def validate_config(self) -> list[str]:
        """Validar configuración y retornar lista de errores"""
        errors = []
        
        # Validar rutas
        ffmpeg_path = self.get_ffmpeg_path()
        if ffmpeg_path and not Path(ffmpeg_path).exists():
            errors.append(f"Ruta de FFmpeg no válida: {ffmpeg_path}")
        
        # Validar valores numéricos
        try:
            season = self.get("series", "default_season", 1)
            if not isinstance(season, int) or season < 1:
                errors.append("Temporada por defecto debe ser un número entero mayor a 0")
        except:
            errors.append("Temporada por defecto no válida")
        
        try:
            episode = self.get("series", "default_start_episode", 1)
            if not isinstance(episode, int) or episode < 1:
                errors.append("Episodio inicial por defecto debe ser un número entero mayor a 0")
        except:
            errors.append("Episodio inicial por defecto no válido")
        
        # Validar opciones de procesamiento
        valid_operations = ["rename", "convert", "extract_audio"]
        operation = self.get("processing", "default_operation", "rename")
        if operation not in valid_operations:
            errors.append(f"Operación por defecto no válida: {operation}")
        
        valid_resolutions = ["Original", "1080p", "720p", "480p"]
        resolution = self.get("processing", "default_resolution", "Original")
        if resolution not in valid_resolutions:
            errors.append(f"Resolución por defecto no válida: {resolution}")
        
        return errors
    
    def __str__(self) -> str:
        """Representación en string de la configuración"""
        return f"ConfigManager(file={self.config_file}, sections={list(self.config.keys())})"
    
    def __repr__(self) -> str:
        return self.__str__()


# Instancia global de configuración
_config_manager = None

def get_config_manager(config_file: str = "config.json") -> ConfigManager:
    """Obtener instancia global del gestor de configuración"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager

def reset_config_manager():
    """Resetear instancia global del gestor de configuración"""
    global _config_manager
    _config_manager = None