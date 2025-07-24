#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana Principal del Organizador de Series
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import json
from pathlib import Path
from datetime import datetime

class MainWindow:
    def __init__(self, controller, config_manager):
        self.controller = controller
        self.config_manager = config_manager
        
        # Estado
        self.video_files = []
        self.is_processing = False
        self.selected_file_index = None
        
        self.setup_window()
        self.create_interface()
        self.check_ffmpeg_status()
        
    def setup_window(self):
        """Configurar la ventana principal"""
        self.root = ctk.CTk()
        self.root.title("📁 Organizador de Series")
        self.root.geometry("1200x900")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables de la interfaz (después de crear la ventana)
        self.source_folder = ctk.StringVar()
        self.output_directory = ctk.StringVar()
        self.series_name = ctk.StringVar()
        self.series_year = ctk.StringVar()
        self.series_id = ctk.StringVar()
        self.season_number = ctk.StringVar(value="1")
        self.start_episode = ctk.StringVar(value="1")
        self.jellyfin_structure = ctk.BooleanVar(value=True)
        self.create_nfo = ctk.BooleanVar(value=True)
        self.search_source = ctk.StringVar(value="tmdb")
        self.metadata_search = ctk.StringVar()
        self.operation_mode = ctk.StringVar(value="rename")
        self.resolution = ctk.StringVar(value="Original")
        self.compression_level = ctk.StringVar(value="Medium")
        self.audio_mode = ctk.StringVar(value="keep_all")
        self.selected_audio_track = ctk.StringVar(value="0")
        self.audio_format = ctk.StringVar(value="mp3")
        
    def create_interface(self):
        """Crear la interfaz principal"""
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, 
                                  text="📁 Organizador de Series",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 30))
        
        # Configuración de carpetas
        self.create_folder_config(main_frame)
        
        # Configuración de serie
        self.create_series_config(main_frame)
        
        # Modo de operación
        self.create_operation_mode(main_frame)
        
        # Lista de archivos
        self.create_files_section(main_frame)
        
        # Progreso
        self.create_progress_section(main_frame)
        
        # Log
        self.create_log_section(main_frame)
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
        # Estado FFmpeg
        self.create_ffmpeg_status(main_frame)
    
    def create_folder_config(self, parent):
        """Crear sección de configuración de carpetas"""
        folder_frame = ctk.CTkFrame(parent)
        folder_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        folder_title = ctk.CTkLabel(folder_frame, text="📂 Configuración de Carpetas", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        folder_title.pack(pady=(15, 10))
        
        # Carpeta origen
        source_frame = ctk.CTkFrame(folder_frame)
        source_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(source_frame, text="Carpeta origen:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        source_entry_frame = ctk.CTkFrame(source_frame)
        source_entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.source_entry = ctk.CTkEntry(source_entry_frame, textvariable=self.source_folder, 
                                        state="readonly")
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(source_entry_frame, text="📁 Seleccionar", 
                     command=self.select_source_folder, width=120).pack(side="left", padx=(0, 5))
        ctk.CTkButton(source_entry_frame, text="🔍 Detectar", 
                     command=self.detect_video_files, width=100).pack(side="left")
        
        # Carpeta destino
        output_frame = ctk.CTkFrame(folder_frame)
        output_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(output_frame, text="Carpeta destino:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        output_entry_frame = ctk.CTkFrame(output_frame)
        output_entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.output_entry = ctk.CTkEntry(output_entry_frame, textvariable=self.output_directory, 
                                        state="readonly")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(output_entry_frame, text="📁 Seleccionar", 
                     command=self.select_output_directory, width=120).pack(side="left")
    
    def create_series_config(self, parent):
        """Crear sección de configuración de serie"""
        config_frame = ctk.CTkFrame(parent)
        config_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        config_title = ctk.CTkLabel(config_frame, text="📝 Configuración de Serie", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        config_title.pack(pady=(15, 10))
        
        # Primera fila: Nombre de serie
        name_frame = ctk.CTkFrame(config_frame)
        name_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(name_frame, text="Nombre de la Serie:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.series_entry = ctk.CTkEntry(name_frame, textvariable=self.series_name, 
                                        placeholder_text="Ej: Breaking Bad")
        self.series_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Segunda fila: Año y ID de metadatos
        metadata_frame = ctk.CTkFrame(config_frame)
        metadata_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        # Año
        year_frame = ctk.CTkFrame(metadata_frame)
        year_frame.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(year_frame, text="Año (opcional):", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.year_entry = ctk.CTkEntry(year_frame, textvariable=self.series_year, 
                                      placeholder_text="2008", width=80)
        self.year_entry.pack(padx=10, pady=(0, 10))
        
        # ID de metadatos
        id_frame = ctk.CTkFrame(metadata_frame)
        id_frame.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=10)
        
        ctk.CTkLabel(id_frame, text="ID Metadatos (opcional):", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.id_entry = ctk.CTkEntry(id_frame, textvariable=self.series_id, 
                                    placeholder_text="tmdbid-12345")
        self.id_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Tercera fila: Temporada y episodio inicial
        numbers_frame = ctk.CTkFrame(config_frame)
        numbers_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Temporada
        season_frame = ctk.CTkFrame(numbers_frame)
        season_frame.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(season_frame, text="Temporada:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.season_entry = ctk.CTkEntry(season_frame, textvariable=self.season_number, width=80)
        self.season_entry.pack(padx=10, pady=(0, 10))
        
        # Episodio inicial
        episode_frame = ctk.CTkFrame(numbers_frame)
        episode_frame.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=10)
        
        ctk.CTkLabel(episode_frame, text="Episodio inicial:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.start_episode_entry = ctk.CTkEntry(episode_frame, textvariable=self.start_episode, width=80)
        self.start_episode_entry.pack(padx=10, pady=(0, 10))
        
        # Cuarta fila: Opciones de Jellyfin
        jellyfin_frame = ctk.CTkFrame(config_frame)
        jellyfin_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(jellyfin_frame, text="🎬 Opciones de Jellyfin:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.jellyfin_check = ctk.CTkCheckBox(jellyfin_frame, text="Usar estructura de carpetas de Jellyfin", 
                                             variable=self.jellyfin_structure)
        self.jellyfin_check.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.nfo_check = ctk.CTkCheckBox(jellyfin_frame, text="Crear archivos .nfo para metadatos", 
                                        variable=self.create_nfo)
        self.nfo_check.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Quinta fila: Búsqueda de metadatos
        search_frame = ctk.CTkFrame(config_frame)
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(search_frame, text="🔍 Búsqueda de Metadatos:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Selector de fuente de búsqueda
        source_frame = ctk.CTkFrame(search_frame)
        source_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        ctk.CTkLabel(source_frame, text="Fuente:", 
                    font=ctk.CTkFont(size=11)).pack(side="left", padx=(10, 5))
        
        self.source_tmdb = ctk.CTkRadioButton(source_frame, text="TMDB", 
                                             variable=self.search_source, value="tmdb",
                                             command=self.on_search_source_change)
        self.source_tmdb.pack(side="left", padx=(0, 10))
        
        self.source_jikan = ctk.CTkRadioButton(source_frame, text="Jikan (MyAnimeList)", 
                                              variable=self.search_source, value="jikan",
                                              command=self.on_search_source_change)
        self.source_jikan.pack(side="left", padx=(0, 10))
        
        search_entry_frame = ctk.CTkFrame(search_frame)
        search_entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(search_entry_frame, textvariable=self.metadata_search, placeholder_text="Buscar serie...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(search_entry_frame, text="🔍 Buscar", 
                     command=self.search_metadata, width=100).pack(side="left")
        
        # Frame para resultados de búsqueda (inicialmente oculto)
        self.search_results_frame = ctk.CTkFrame(search_frame)
        
        ctk.CTkLabel(self.search_results_frame, text="Resultados de búsqueda:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.results_scroll = ctk.CTkScrollableFrame(self.search_results_frame, height=150)
        self.results_scroll.pack(fill="x", padx=10, pady=(0, 10))
    
    def create_operation_mode(self, parent):
        """Crear sección de modo de operación"""
        mode_frame = ctk.CTkFrame(parent)
        mode_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        mode_title = ctk.CTkLabel(mode_frame, text="⚙️ Modo de Operación", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        mode_title.pack(pady=(15, 10))
        
        # Radiobuttons para modo
        mode_buttons_frame = ctk.CTkFrame(mode_frame)
        mode_buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.mode_rename = ctk.CTkRadioButton(mode_buttons_frame, text="🏷️ Solo renombrar archivos", 
                                             variable=self.operation_mode, value="rename",
                                             command=self.on_mode_change)
        self.mode_rename.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.mode_convert = ctk.CTkRadioButton(mode_buttons_frame, text="🔄 Convertir y renombrar", 
                                              variable=self.operation_mode, value="convert",
                                              command=self.on_mode_change)
        self.mode_convert.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.mode_extract = ctk.CTkRadioButton(mode_buttons_frame, text="🎵 Extraer audio y renombrar", 
                                              variable=self.operation_mode, value="extract_audio",
                                              command=self.on_mode_change)
        self.mode_extract.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Frame de opciones de compresión (inicialmente oculto)
        self.compression_frame = ctk.CTkFrame(mode_frame)
        
        # Resolución
        resolution_frame = ctk.CTkFrame(self.compression_frame)
        resolution_frame.pack(fill="x", pady=(15, 10), padx=15)
        
        ctk.CTkLabel(resolution_frame, text="Resolución:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.resolution_combo = ctk.CTkComboBox(resolution_frame, variable=self.resolution, 
                                               values=["Original", "1080p", "720p", "480p"], 
                                               state="readonly", width=150)
        self.resolution_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Nivel de compresión
        compression_frame_inner = ctk.CTkFrame(self.compression_frame)
        compression_frame_inner.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(compression_frame_inner, text="Compresión:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.compression_combo = ctk.CTkComboBox(compression_frame_inner, variable=self.compression_level,
                                                values=["Low (Alta calidad)", "Medium (Balanceado)", "High (Menor tamaño)"],
                                                state="readonly", width=200)
        self.compression_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Frame de opciones de audio (inicialmente oculto)
        self.audio_frame = ctk.CTkFrame(mode_frame)
        
        # Modo de audio
        audio_mode_frame = ctk.CTkFrame(self.audio_frame)
        audio_mode_frame.pack(fill="x", pady=(15, 10), padx=15)
        
        ctk.CTkLabel(audio_mode_frame, text="Manejo de Audio:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.audio_keep_all = ctk.CTkRadioButton(audio_mode_frame, text="Mantener todas las pistas", 
                                                variable=self.audio_mode, value="keep_all",
                                                command=self.on_audio_mode_change)
        self.audio_keep_all.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.audio_select = ctk.CTkRadioButton(audio_mode_frame, text="Seleccionar pista específica", 
                                              variable=self.audio_mode, value="select_track",
                                              command=self.on_audio_mode_change)
        self.audio_select.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.audio_extract_all = ctk.CTkRadioButton(audio_mode_frame, text="Extraer todas las pistas como archivos separados", 
                                                   variable=self.audio_mode, value="extract_all",
                                                   command=self.on_audio_mode_change)
        self.audio_extract_all.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Opciones específicas de audio
        self.audio_options_frame = ctk.CTkFrame(self.audio_frame)
        
        # Selección de pista
        track_frame = ctk.CTkFrame(self.audio_options_frame)
        track_frame.pack(fill="x", pady=(15, 10), padx=15)
        
        ctk.CTkLabel(track_frame, text="Pista de audio:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.audio_track_combo = ctk.CTkComboBox(track_frame, variable=self.selected_audio_track, 
                                                values=["0", "1", "2", "3"], 
                                                state="readonly", width=100)
        self.audio_track_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Formato de audio
        format_frame = ctk.CTkFrame(self.audio_options_frame)
        format_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(format_frame, text="Formato de audio:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.format_combo = ctk.CTkComboBox(format_frame, variable=self.audio_format,
                                           values=["mp3", "wav"],
                                           state="readonly", width=100)
        self.format_combo.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Inicialmente ocultar opciones de conversión
        self.on_mode_change()
    
    def create_files_section(self, parent):
        """Crear sección de archivos"""
        files_frame = ctk.CTkFrame(parent)
        files_frame.pack(fill="both", expand=True, pady=(0, 20), padx=10)
        
        files_title = ctk.CTkLabel(files_frame, text="📋 Archivos Detectados", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        files_title.pack(pady=(15, 10))
        
        # Frame para la tabla y scrollbar
        table_frame = ctk.CTkFrame(files_frame)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Crear un frame scrollable para simular treeview
        self.files_scroll_frame = ctk.CTkScrollableFrame(table_frame, height=200)
        self.files_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(self.files_scroll_frame)
        headers_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(headers_frame, text="#", width=50, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Archivo Original", width=300, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Nuevo Nombre", width=300, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Tamaño", width=100, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        
        # Frame de botones para manipular lista
        buttons_frame = ctk.CTkFrame(files_frame)
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(buttons_frame, text="🔼 Subir", command=self.move_file_up, 
                     width=80).pack(side="left", padx=(10, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🔽 Bajar", command=self.move_file_down, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🔄 Actualizar Nombres", command=self.update_file_names, 
                     width=150).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🗑️ Quitar", command=self.remove_file, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
    
    def create_progress_section(self, parent):
        """Crear sección de progreso"""
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        progress_title = ctk.CTkLabel(progress_frame, text="📊 Progreso", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        progress_title.pack(pady=(15, 10))
        
        progress_inner_frame = ctk.CTkFrame(progress_frame)
        progress_inner_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Progreso general
        self.progress_label = ctk.CTkLabel(progress_inner_frame, text="Listo para procesar", 
                                          font=ctk.CTkFont(size=12))
        self.progress_label.pack(pady=(15, 5))
        
        self.overall_progress = ctk.CTkProgressBar(progress_inner_frame)
        self.overall_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.overall_progress.set(0)
        
        # Progreso del archivo actual
        self.file_label = ctk.CTkLabel(progress_inner_frame, text="", 
                                      font=ctk.CTkFont(size=11))
        self.file_label.pack(pady=(0, 5))
        
        self.current_progress = ctk.CTkProgressBar(progress_inner_frame)
        self.current_progress.pack(fill="x", padx=15, pady=(0, 15))
        self.current_progress.set(0)
    
    def create_log_section(self, parent):
        """Crear sección de log"""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, pady=(0, 20), padx=10)
        
        log_title = ctk.CTkLabel(log_frame, text="📝 Registro de Actividad", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=(15, 10))
        
        # Frame para log
        log_container = ctk.CTkFrame(log_frame)
        log_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.log_text = ctk.CTkTextbox(log_container, height=150, 
                                      font=ctk.CTkFont(family="Consolas", size=11))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón para limpiar log
        ctk.CTkButton(log_frame, text="🗑️ Limpiar Log", command=self.clear_log, 
                     width=120).pack(pady=(0, 15))
    
    def create_action_buttons(self, parent):
        """Crear botones de acción"""
        action_frame = ctk.CTkFrame(parent)
        action_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        action_title = ctk.CTkLabel(action_frame, text="🎬 Acciones", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        action_title.pack(pady=(15, 10))
        
        buttons_container = ctk.CTkFrame(action_frame)
        buttons_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # Botón principal
        self.process_button = ctk.CTkButton(buttons_container, text="🚀 Iniciar Procesamiento", 
                                           command=self.start_processing,
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           height=40, width=180)
        self.process_button.pack(side="left", padx=(15, 10), pady=15)
        
        # Botón detener
        self.stop_button = ctk.CTkButton(buttons_container, text="⏹️ Detener", 
                                        command=self.stop_processing, state="disabled",
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        height=40, width=120)
        self.stop_button.pack(side="left", padx=10, pady=15)
        
        # Botón volver al menú
        ctk.CTkButton(buttons_container, text="🏠 Menú Principal", 
                     command=self.back_to_menu,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     height=40, width=150).pack(side="right", padx=(10, 15), pady=15)
    
    def create_ffmpeg_status(self, parent):
        """Crear indicador de estado de FFmpeg"""
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        self.ffmpeg_status_label = ctk.CTkLabel(status_frame, text="🔍 Buscando FFmpeg...", 
                                                font=ctk.CTkFont(size=12),
                                                text_color="orange")
        self.ffmpeg_status_label.pack(pady=15)
        
    def check_ffmpeg_status(self):
        """Verificar el estado de FFmpeg"""
        try:
            # Usar el controlador para verificar FFmpeg
            if hasattr(self.controller, 'model') and hasattr(self.controller.model, 'ffmpeg_path'):
                if self.controller.model.ffmpeg_path:
                    self.ffmpeg_status_label.configure(
                        text="✅ FFmpeg detectado correctamente",
                        text_color="green"
                    )
                    self.log_message(f"✅ FFmpeg encontrado en: {self.controller.model.ffmpeg_path}")
                else:
                    self.ffmpeg_status_label.configure(
                        text="❌ FFmpeg no encontrado",
                        text_color="red"
                    )
                    self.log_message("❌ FFmpeg no encontrado. Verifica la instalación.")
            else:
                # Fallback: verificar usando utils
                from pathlib import Path
                import subprocess
                
                # Rutas posibles para FFmpeg
                possible_paths = [
                    "ffmpeg",
                    "bin/ffmpeg.exe",
                    "./bin/ffmpeg.exe",
                    str(Path(__file__).parent.parent / "bin" / "ffmpeg.exe"),
                    "ffmpeg/bin/ffmpeg.exe",
                    "./ffmpeg/bin/ffmpeg.exe",
                    "../bin/ffmpeg.exe",
                    "../ffmpeg/bin/ffmpeg.exe"
                ]
                
                ffmpeg_found = False
                for path in possible_paths:
                    try:
                        result = subprocess.run([path, "-version"], 
                                               capture_output=True, 
                                               text=True, 
                                               timeout=5)
                        if result.returncode == 0:
                            self.ffmpeg_status_label.configure(
                                text="✅ FFmpeg detectado correctamente",
                                text_color="green"
                            )
                            self.log_message(f"✅ FFmpeg encontrado en: {path}")
                            ffmpeg_found = True
                            break
                    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                        continue
                
                if not ffmpeg_found:
                    self.ffmpeg_status_label.configure(
                        text="❌ FFmpeg no encontrado",
                        text_color="red"
                    )
                    self.log_message("❌ FFmpeg no encontrado. Verifica la instalación.")
                    
        except Exception as e:
            self.ffmpeg_status_label.configure(
                text="❌ Error al verificar FFmpeg",
                text_color="red"
            )
            self.log_message(f"❌ Error al verificar FFmpeg: {e}")
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert("end", formatted_message)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Limpiar el log"""
        self.log_text.delete("0.0", "end")
    
    # Métodos de interfaz que delegan al controlador
    def select_source_folder(self):
        """Seleccionar carpeta origen"""
        folder = filedialog.askdirectory(title="Seleccionar Carpeta de Videos")
        if folder:
            self.source_folder.set(folder)
            self.log_message(f"📁 Carpeta origen seleccionada: {folder}")
    
    def select_output_directory(self):
        """Seleccionar directorio de salida"""
        directory = filedialog.askdirectory(title="Seleccionar Carpeta de Destino")
        if directory:
            self.output_directory.set(directory)
            self.log_message(f"📁 Carpeta destino seleccionada: {directory}")
    
    def detect_video_files(self):
        """Detectar archivos de video"""
        if not self.source_folder.get():
            messagebox.showwarning("Advertencia", "Selecciona primero una carpeta origen")
            return
        
        # Delegar al controlador
        self.video_files = self.controller.detect_video_files(self.source_folder.get())
        self.refresh_files_display()
        self.log_message(f"🔍 Detectados {len(self.video_files)} archivos de video")
    
    def refresh_files_display(self):
        """Actualizar la visualización de archivos"""
        # Limpiar frame actual
        for widget in self.files_scroll_frame.winfo_children():
            if not isinstance(widget, ctk.CTkFrame) or widget == self.files_scroll_frame.winfo_children()[0]:  # Mantener headers
                continue
            widget.destroy()
        
        # Recrear lista
        for i, video_file in enumerate(self.video_files):
            file_frame = ctk.CTkFrame(self.files_scroll_frame)
            file_frame.pack(fill="x", pady=2)
            
            # Número
            episode_label = ctk.CTkLabel(file_frame, text=str(video_file.episode_number), width=50)
            episode_label.pack(side="left", padx=5)
            episode_label.bind("<Double-Button-1>", lambda e, idx=i: self.edit_episode_number(idx))
            
            # Archivo original
            original_text = video_file.original_name[:40] + "..." if len(video_file.original_name) > 40 else video_file.original_name
            ctk.CTkLabel(file_frame, text=original_text, width=300).pack(side="left", padx=5)
            
            # Nuevo nombre
            new_text = video_file.new_name[:40] + "..." if len(video_file.new_name) > 40 else video_file.new_name
            ctk.CTkLabel(file_frame, text=new_text, width=300).pack(side="left", padx=5)
            
            # Tamaño
            ctk.CTkLabel(file_frame, text=video_file.size_str, width=100).pack(side="left", padx=5)
    
    def edit_episode_number(self, index):
        """Editar número de episodio"""
        if index >= len(self.video_files):
            return
            
        current_episode = self.video_files[index].episode_number
        
        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Editar Episodio")
        dialog.geometry("500x320")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar la ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Contenido del diálogo
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Editar Episodio", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Información del archivo
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(info_frame, text="Archivo:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(info_frame, text=self.video_files[index].original_name, 
                    font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=(0, 10))
        
        # Pestañas para diferentes opciones
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(fill="both", expand=True, pady=(0, 20))
        
        # Pestaña 1: Cambiar número de episodio
        tab1 = tabview.add("Número de Episodio")
        
        ctk.CTkLabel(tab1, text="Nuevo número de episodio:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 10))
        
        episode_var = ctk.StringVar(value=str(current_episode))
        episode_entry = ctk.CTkEntry(tab1, textvariable=episode_var, width=100, justify='center')
        episode_entry.pack(pady=(0, 20))
        episode_entry.select_range(0, 'end')
        episode_entry.focus()
        
        # Pestaña 2: Cambiar posición en la lista
        tab2 = tabview.add("Posición en Lista")
        
        ctk.CTkLabel(tab2, text="Nueva posición en la lista:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 10))
        
        position_var = ctk.StringVar(value=str(index + 1))
        position_entry = ctk.CTkEntry(tab2, textvariable=position_var, width=100, justify='center')
        position_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(tab2, text=f"(1 a {len(self.video_files)})", 
                    font=ctk.CTkFont(size=10)).pack()
        
        def save_episode():
            try:
                active_tab = tabview.get()
                
                if active_tab == "Número de Episodio":
                    new_episode = int(episode_var.get())
                    if new_episode < 1:
                        messagebox.showerror("Error", "El número de episodio debe ser mayor a 0.")
                        return
                    
                    # Actualizar episodio
                    self.video_files[index].episode_number = new_episode
                    self.video_files[index].update_new_name(
                        self.series_name.get(),
                        int(self.season_number.get()),
                        new_episode
                    )
                    self.log_message(f"✏️ Episodio actualizado: {self.video_files[index].original_name} -> Episodio {new_episode}")
                    
                elif active_tab == "Posición en Lista":
                    new_position = int(position_var.get())
                    if new_position < 1 or new_position > len(self.video_files):
                        messagebox.showerror("Error", f"La posición debe estar entre 1 y {len(self.video_files)}.")
                        return
                    
                    # Mover archivo a nueva posición
                    file_to_move = self.video_files.pop(index)
                    self.video_files.insert(new_position - 1, file_to_move)
                    self.log_message(f"📋 Archivo movido a posición {new_position}: {file_to_move.original_name}")
                
                self.refresh_files_display()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número válido.")
        
        def cancel():
            dialog.destroy()
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(buttons_frame, text="💾 Guardar", command=save_episode, 
                     width=100).pack(side="left", padx=(0, 10), pady=10)
        ctk.CTkButton(buttons_frame, text="❌ Cancelar", command=cancel, 
                     width=100).pack(side="left", pady=10)
        
        # Bind Enter y Escape
        dialog.bind('<Return>', lambda e: save_episode())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def move_file_up(self):
        """Mover archivo seleccionado hacia arriba"""
        if self.selected_file_index is not None and self.selected_file_index > 0:
            # Intercambiar archivos
            self.video_files[self.selected_file_index], self.video_files[self.selected_file_index - 1] = \
                self.video_files[self.selected_file_index - 1], self.video_files[self.selected_file_index]
            self.selected_file_index -= 1
            self.refresh_files_display()
            self.log_message("🔼 Archivo movido hacia arriba")
    
    def move_file_down(self):
        """Mover archivo seleccionado hacia abajo"""
        if self.selected_file_index is not None and self.selected_file_index < len(self.video_files) - 1:
            # Intercambiar archivos
            self.video_files[self.selected_file_index], self.video_files[self.selected_file_index + 1] = \
                self.video_files[self.selected_file_index + 1], self.video_files[self.selected_file_index]
            self.selected_file_index += 1
            self.refresh_files_display()
            self.log_message("🔽 Archivo movido hacia abajo")
    
    def update_file_names(self):
        """Actualizar nombres de archivos"""
        if not self.series_name.get().strip():
            messagebox.showwarning("Advertencia", "Ingresa el nombre de la serie")
            return
        
        series_name = self.series_name.get().strip()
        season = int(self.season_number.get())
        start_episode = int(self.start_episode.get())
        
        for i, video_file in enumerate(self.video_files):
            episode_num = start_episode + i
            video_file.update_new_name(series_name, season, episode_num)
        
        self.refresh_files_display()
        self.log_message("🔄 Nombres de archivos actualizados")
    
    def remove_file(self):
        """Eliminar archivo seleccionado"""
        if self.selected_file_index is not None:
            removed_file = self.video_files.pop(self.selected_file_index)
            self.selected_file_index = None
            self.refresh_files_display()
            self.log_message(f"🗑️ Archivo eliminado: {removed_file.original_name}")
    
    def on_search_source_change(self):
        """Cambio en la fuente de búsqueda"""
        pass
    
    def search_metadata(self):
        """Buscar metadatos"""
        query = self.metadata_search.get().strip()
        if not query:
            messagebox.showwarning("Advertencia", "Ingresa un término de búsqueda")
            return
        
        # Delegar al controlador
        self.controller.search_metadata(query, self.search_source.get())
    
    def on_mode_change(self):
        """Cambio en el modo de operación"""
        mode = self.operation_mode.get()
        
        # Ocultar todos los frames de opciones
        self.compression_frame.pack_forget()
        self.audio_frame.pack_forget()
        
        if mode == "convert":
            self.compression_frame.pack(fill="x", padx=15, pady=(0, 15))
        elif mode == "extract_audio":
            self.audio_frame.pack(fill="x", padx=15, pady=(0, 15))
            self.on_audio_mode_change()
    
    def on_audio_mode_change(self):
        """Cambio en el modo de audio"""
        mode = self.audio_mode.get()
        
        # Ocultar opciones específicas
        self.audio_options_frame.pack_forget()
        
        if mode == "select_track" or mode == "extract_all":
            self.audio_options_frame.pack(fill="x", padx=15, pady=(0, 15))
    
    def start_processing(self):
        """Iniciar procesamiento"""
        if not self.video_files:
            messagebox.showwarning("Advertencia", "No hay archivos para procesar")
            return
        
        if not self.series_name.get().strip():
            messagebox.showwarning("Advertencia", "Ingresa el nombre de la serie")
            return
        
        if not self.output_directory.get():
            messagebox.showwarning("Advertencia", "Selecciona una carpeta de destino")
            return
        
        self.is_processing = True
        self.process_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Iniciar procesamiento en hilo separado
        threading.Thread(target=self._process_files, daemon=True).start()
    
    def _process_files(self):
        """Proceso de archivos en hilo separado"""
        try:
            # Delegar al controlador
            self.controller.process_files(
                self.video_files,
                self.output_directory.get(),
                self.operation_mode.get(),
                {
                    'series_name': self.series_name.get(),
                    'season': int(self.season_number.get()),
                    'jellyfin_structure': self.jellyfin_structure.get(),
                    'create_nfo': self.create_nfo.get(),
                    'resolution': self.resolution.get(),
                    'compression': self.compression_level.get(),
                    'audio_mode': self.audio_mode.get(),
                    'audio_track': self.selected_audio_track.get(),
                    'audio_format': self.audio_format.get()
                },
                self._update_progress,
                self.log_message
            )
        except Exception as e:
            self.log_message(f"❌ Error durante el procesamiento: {e}")
        finally:
            self.is_processing = False
            self.root.after(0, self._reset_processing_ui)
    
    def _update_progress(self, current, total, current_file=""):
        """Actualizar progreso"""
        progress = current / total if total > 0 else 0
        self.root.after(0, lambda: self.overall_progress.set(progress))
        self.root.after(0, lambda: self.progress_label.configure(
            text=f"Procesando archivo {current} de {total}"))
        if current_file:
            self.root.after(0, lambda: self.file_label.configure(text=current_file))
    
    def _reset_processing_ui(self):
        """Resetear UI después del procesamiento"""
        self.process_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_label.configure(text="Procesamiento finalizado")
        self.file_label.configure(text="")
    
    def stop_processing(self):
        """Detener procesamiento"""
        self.is_processing = False
        self.controller.stop_processing()
        self.log_message("⏹️ Procesamiento detenido por el usuario")
    
    def back_to_menu(self):
        """Volver al menú principal"""
        if self.is_processing:
            if messagebox.askyesno("Confirmar", "¿Detener el procesamiento y volver al menú?"):
                self.stop_processing()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Ejecutar la aplicación"""
        self.center_window()
        self.root.mainloop()