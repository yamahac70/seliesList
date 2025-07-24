#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana del Convertidor de Series M3U8
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import json
from pathlib import Path
from datetime import datetime

class SeriesConverterWindow:
    def __init__(self, controller, config_manager, parent=None):
        self.controller = controller
        self.config_manager = config_manager
        self.parent = parent
        
        # Estado
        self.episodes_list = []
        self.is_converting = False
        self.current_episode = 0
        self.total_episodes = 0
        
        self.setup_window()
        self.create_interface()
        self.check_ffmpeg_status()
        
    def setup_window(self):
        """Configurar la ventana principal"""
        self.root = ctk.CTk()
        self.root.title("📺 M3U8 to MP4 Converter - Modo Serie")
        self.root.geometry("1000x800")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables de la interfaz (después de crear la ventana)
        self.series_name = ctk.StringVar()
        self.season_number = ctk.StringVar(value="01")
        self.start_episode = ctk.StringVar(value="01")
        self.resolution = ctk.StringVar(value="Original")
        self.compression_level = ctk.StringVar(value="Medium")
        self.output_directory = ctk.StringVar(value=str(Path.cwd()))
        self.episode_url_var = ctk.StringVar()
        self.episode_name_var = ctk.StringVar()
        
    def create_interface(self):
        """Crear la interfaz principal"""
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, 
                                  text="📺 Convertidor de Series M3U8",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 30))
        
        # Configuración de serie
        self.create_series_config(main_frame)
        
        # Lista de episodios
        self.create_episodes_section(main_frame)
        
        # Configuración de video
        self.create_video_config(main_frame)
        
        # Progreso
        self.create_progress_section(main_frame)
        
        # Log
        self.create_log_section(main_frame)
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
        # Estado FFmpeg
        self.create_ffmpeg_status(main_frame)
        
    def create_series_config(self, parent):
        """Crear sección de configuración de serie"""
        config_frame = ctk.CTkFrame(parent)
        config_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        config_title = ctk.CTkLabel(config_frame, text="📝 Configuración de Serie", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        config_title.pack(pady=(15, 10))
        
        # Nombre de serie
        name_frame = ctk.CTkFrame(config_frame)
        name_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(name_frame, text="Nombre de la Serie:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.series_entry = ctk.CTkEntry(name_frame, textvariable=self.series_name, 
                                        placeholder_text="Ej: Breaking Bad")
        self.series_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Temporada y episodio inicial
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
        
        # Carpeta destino
        output_frame = ctk.CTkFrame(config_frame)
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
        
    def create_episodes_section(self, parent):
        """Crear sección de episodios"""
        episodes_frame = ctk.CTkFrame(parent)
        episodes_frame.pack(fill="both", expand=True, pady=(0, 20), padx=10)
        
        episodes_title = ctk.CTkLabel(episodes_frame, text="📋 Lista de Episodios", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        episodes_title.pack(pady=(15, 10))
        
        # Frame para agregar episodio
        add_frame = ctk.CTkFrame(episodes_frame)
        add_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # URL del episodio
        url_frame = ctk.CTkFrame(add_frame)
        url_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(url_frame, text="URL M3U8:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.url_entry = ctk.CTkEntry(url_frame, textvariable=self.episode_url_var, 
                                     placeholder_text="https://ejemplo.com/episodio.m3u8")
        self.url_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Nombre del episodio
        name_frame = ctk.CTkFrame(add_frame)
        name_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(name_frame, text="Nombre del Episodio (opcional):", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.episode_name_var, 
                                      placeholder_text="Ej: El Piloto")
        self.name_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botón agregar
        ctk.CTkButton(add_frame, text="➕ Agregar Episodio", 
                     command=self.add_episode, width=150).pack(pady=10)
        
        # Lista de episodios
        list_frame = ctk.CTkFrame(episodes_frame)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Frame scrollable para la lista
        self.episodes_scroll_frame = ctk.CTkScrollableFrame(list_frame, height=200)
        self.episodes_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(self.episodes_scroll_frame)
        headers_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(headers_frame, text="Episodio", width=80, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Nombre", width=250, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="URL", width=300, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        
        # Botones para manejar lista
        buttons_frame = ctk.CTkFrame(episodes_frame)
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(buttons_frame, text="🔼 Subir", command=self.move_episode_up, 
                     width=80).pack(side="left", padx=(10, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🔽 Bajar", command=self.move_episode_down, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="✏️ Editar", command=self.edit_episode, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🗑️ Eliminar", command=self.remove_episode, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="🔄 Limpiar", command=self.clear_episodes, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="📁 Cargar", command=self.load_episodes_file, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        ctk.CTkButton(buttons_frame, text="💾 Guardar", command=self.save_episodes_file, 
                     width=80).pack(side="left", padx=(0, 5), pady=10)
        
    def create_video_config(self, parent):
        """Crear sección de configuración de video"""
        video_frame = ctk.CTkFrame(parent)
        video_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        video_title = ctk.CTkLabel(video_frame, text="🎥 Configuración de Video", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        video_title.pack(pady=(15, 10))
        
        config_inner_frame = ctk.CTkFrame(video_frame)
        config_inner_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Resolución
        resolution_frame = ctk.CTkFrame(config_inner_frame)
        resolution_frame.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(resolution_frame, text="Resolución:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.resolution_combo = ctk.CTkComboBox(resolution_frame, variable=self.resolution, 
                                               values=["Original", "1080p", "720p", "480p", "360p"], 
                                               state="readonly", width=150)
        self.resolution_combo.pack(padx=10, pady=(0, 10))
        
        # Compresión
        compression_frame = ctk.CTkFrame(config_inner_frame)
        compression_frame.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=10)
        
        ctk.CTkLabel(compression_frame, text="Compresión:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.compression_combo = ctk.CTkComboBox(compression_frame, variable=self.compression_level,
                                                values=["None", "Low", "Medium", "High", "Maximum"],
                                                state="readonly", width=150)
        self.compression_combo.pack(padx=10, pady=(0, 10))
        
    def create_progress_section(self, parent):
        """Crear sección de progreso"""
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        progress_title = ctk.CTkLabel(progress_frame, text="📊 Progreso de Conversión", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        progress_title.pack(pady=(15, 10))
        
        progress_inner_frame = ctk.CTkFrame(progress_frame)
        progress_inner_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Progreso general
        self.status_label = ctk.CTkLabel(progress_inner_frame, text="Listo para comenzar", 
                                        font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(15, 5))
        
        self.overall_progress = ctk.CTkProgressBar(progress_inner_frame)
        self.overall_progress.pack(fill="x", padx=15, pady=(0, 10))
        self.overall_progress.set(0)
        
        # Progreso del episodio actual
        self.episode_label = ctk.CTkLabel(progress_inner_frame, text="", 
                                         font=ctk.CTkFont(size=11))
        self.episode_label.pack(pady=(0, 5))
        
        self.episode_progress = ctk.CTkProgressBar(progress_inner_frame)
        self.episode_progress.pack(fill="x", padx=15, pady=(0, 15))
        self.episode_progress.set(0)
        
    def create_log_section(self, parent):
        """Crear sección de log"""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, pady=(0, 20), padx=10)
        
        log_title = ctk.CTkLabel(log_frame, text="📝 Log de Conversión", 
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
        self.start_button = ctk.CTkButton(buttons_container, text="🚀 Iniciar Conversión", 
                                         command=self.start_conversion,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         height=40, width=180)
        self.start_button.pack(side="left", padx=(15, 10), pady=15)
        
        # Botón detener
        self.stop_button = ctk.CTkButton(buttons_container, text="⏹️ Detener", 
                                        command=self.stop_conversion, state="disabled",
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
                    str(Path(__file__).parent.parent.parent / "bin" / "ffmpeg.exe"),
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
        
    # Métodos de manejo de episodios
    def add_episode(self):
        """Agregar episodio a la lista"""
        url = self.episode_url_var.get().strip()
        name = self.episode_name_var.get().strip()
        
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL M3U8")
            return
        
        if not name:
            start_num = int(self.start_episode.get())
            name = f"Episodio {start_num + len(self.episodes_list)}"
        
        start_num = int(self.start_episode.get())
        episode_num = f"{start_num + len(self.episodes_list):02d}"
        episode_data = {
            'number': episode_num,
            'name': name,
            'url': url
        }
        
        self.episodes_list.append(episode_data)
        self.refresh_episodes_display()
        
        # Limpiar campos
        self.episode_url_var.set('')
        self.episode_name_var.set('')
        
        self.log_message(f"✅ Episodio {episode_num} agregado: {name}")
        
    def refresh_episodes_display(self):
        """Actualizar la visualización de episodios"""
        # Limpiar frame actual
        for widget in self.episodes_scroll_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.episodes_scroll_frame.winfo_children()[0]:  # Mantener headers
                widget.destroy()
        
        # Recrear lista
        for i, episode in enumerate(self.episodes_list):
            episode_frame = ctk.CTkFrame(self.episodes_scroll_frame)
            episode_frame.pack(fill="x", pady=2)
            
            # Número de episodio
            ctk.CTkLabel(episode_frame, text=episode['number'], width=80).pack(side="left", padx=5)
            
            # Nombre
            name_text = episode['name'][:30] + "..." if len(episode['name']) > 30 else episode['name']
            ctk.CTkLabel(episode_frame, text=name_text, width=250).pack(side="left", padx=5)
            
            # URL (truncada)
            url_text = episode['url'][:40] + "..." if len(episode['url']) > 40 else episode['url']
            ctk.CTkLabel(episode_frame, text=url_text, width=300).pack(side="left", padx=5)
            
    def move_episode_up(self):
        """Mover episodio seleccionado hacia arriba"""
        # Implementar lógica de selección y movimiento
        pass
        
    def move_episode_down(self):
        """Mover episodio seleccionado hacia abajo"""
        # Implementar lógica de selección y movimiento
        pass
        
    def edit_episode(self):
        """Editar episodio seleccionado"""
        # Implementar diálogo de edición
        pass
        
    def remove_episode(self):
        """Eliminar episodio seleccionado"""
        # Implementar eliminación
        pass
        
    def clear_episodes(self):
        """Limpiar todos los episodios"""
        self.episodes_list.clear()
        self.refresh_episodes_display()
        self.log_message("🗑️ Lista de episodios limpiada")
        
    def load_episodes_file(self):
        """Cargar lista de episodios desde archivo"""
        file_path = filedialog.askopenfilename(
            title="Cargar Lista de Episodios",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.episodes_list = json.load(f)
                self.refresh_episodes_display()
                self.log_message(f"📁 Lista cargada desde {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {e}")
                
    def save_episodes_file(self):
        """Guardar lista de episodios a archivo"""
        if not self.episodes_list:
            messagebox.showwarning("Advertencia", "No hay episodios para guardar")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Guardar Lista de Episodios",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.episodes_list, f, indent=2, ensure_ascii=False)
                self.log_message(f"💾 Lista guardada en {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar archivo: {e}")
                
    def select_output_directory(self):
        """Seleccionar directorio de salida"""
        directory = filedialog.askdirectory(title="Seleccionar Carpeta de Destino")
        if directory:
            self.output_directory.set(directory)
            self.log_message(f"📁 Carpeta destino: {directory}")
            
    def start_conversion(self):
        """Iniciar conversión de episodios"""
        if not self.episodes_list:
            messagebox.showwarning("Advertencia", "No hay episodios para convertir")
            return
            
        if not self.series_name.get().strip():
            messagebox.showwarning("Advertencia", "Ingresa el nombre de la serie")
            return
            
        self.is_converting = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Iniciar conversión en hilo separado
        threading.Thread(target=self._convert_episodes, daemon=True).start()
        
    def _convert_episodes(self):
        """Proceso de conversión en hilo separado"""
        try:
            self.total_episodes = len(self.episodes_list)
            
            # Crear directorio de la serie
            series_dir = Path(self.output_directory.get()) / self.series_name.get().strip()
            series_dir.mkdir(parents=True, exist_ok=True)
            
            self.root.after(0, lambda: self.log_message(f"📁 Directorio de serie: {series_dir}"))
            
            for i, episode in enumerate(self.episodes_list):
                if not self.is_converting:
                    break
                    
                self.current_episode = i + 1
                
                # Actualizar UI
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"Convirtiendo episodio {self.current_episode} de {self.total_episodes}"))
                self.root.after(0, lambda: self.episode_label.configure(
                    text=f"Episodio {episode['number']}: {episode['name']}"))
                
                # Generar nombre de archivo
                season = self.season_number.get().zfill(2)
                episode_num = episode['number']
                filename = f"{self.series_name.get().strip()} {season}x{episode_num}.mp4"
                output_path = series_dir / filename
                
                self.root.after(0, lambda: self.log_message(f"🎬 Iniciando conversión: {episode['name']}"))
                self.root.after(0, lambda: self.log_message(f"📄 Archivo de salida: {output_path.name}"))
                
                # Conversión real usando FFmpeg
                success = self._convert_single_episode(episode['url'], output_path)
                
                if success:
                    self.root.after(0, lambda: self.log_message(f"✅ Completado: {episode['name']}"))
                else:
                    self.root.after(0, lambda: self.log_message(f"❌ Error al convertir: {episode['name']}"))
                
                # Actualizar progreso general
                progress = (i + 1) / self.total_episodes
                self.root.after(0, lambda p=progress: self.overall_progress.set(p))
                
            if self.is_converting:
                self.root.after(0, lambda: self.log_message("🎉 ¡Conversión de serie completada!"))
                self.root.after(0, lambda: self.log_message(f"📁 Archivos guardados en: {series_dir}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Error durante la conversión: {e}"))
        finally:
            self.is_converting = False
            self.root.after(0, self._reset_conversion_ui)
            
    def _reset_conversion_ui(self):
        """Resetear UI después de conversión"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Conversión finalizada")
        self.episode_label.configure(text="")
        self.overall_progress.set(0)
        self.episode_progress.set(0)
        
    def _convert_single_episode(self, url, output_path):
        """Convertir un episodio individual usando FFmpeg con progreso en tiempo real"""
        try:
            # Importar FFmpegProcessor para verificar disponibilidad
            import sys
            import os
            import subprocess
            import re
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from app.utils import FFmpegProcessor
            
            # Crear procesador FFmpeg
            ffmpeg = FFmpegProcessor()
            
            if not ffmpeg.is_available():
                self.root.after(0, lambda: self.log_message("❌ FFmpeg no está disponible"))
                return False
            
            # Configurar parámetros de conversión
            resolution = self.resolution.get()
            compression_level = self.compression_level.get()
            
            self.root.after(0, lambda: self.log_message(f"⚙️ Configuración: {resolution}, Compresión: {compression_level}"))
            
            # Resetear progreso del episodio
            self.root.after(0, lambda: self.episode_progress.set(0))
            
            # Generar comando FFmpeg
            cmd = self._get_ffmpeg_command(ffmpeg.ffmpeg_path, url, str(output_path))
            
            self.root.after(0, lambda: self.log_message(f"🔧 Comando: {' '.join(cmd)}"))
            
            # Ejecutar FFmpeg con progreso en tiempo real
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            total_duration = 0
            
            # Leer salida en tiempo real
            while True:
                if not self.is_converting:
                    process.terminate()
                    return False
                
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    line = output.strip()
                    
                    # Parsear duración total
                    if "Duration:" in line and total_duration == 0:
                        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', line)
                        if duration_match:
                            hours, minutes, seconds, centiseconds = map(int, duration_match.groups())
                            total_duration = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
                    
                    # Parsear progreso
                    if "time=" in line and total_duration > 0:
                        time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})', line)
                        if time_match:
                            hours, minutes, seconds, centiseconds = map(int, time_match.groups())
                            current_time = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
                            progress = min((current_time / total_duration), 1.0)
                            self.root.after(0, lambda p=progress: self.episode_progress.set(p))
                    
                    # Mostrar log con categorización
                    if line and not line.startswith('frame='):
                        if 'error' in line.lower():
                            self.root.after(0, lambda l=line: self.log_message(f"❌ {l}"))
                        elif 'warning' in line.lower():
                            self.root.after(0, lambda l=line: self.log_message(f"⚠️ {l}"))
                        elif any(keyword in line.lower() for keyword in ['duration', 'stream', 'video:', 'audio:', 'input #', 'output #']):
                            self.root.after(0, lambda l=line: self.log_message(f"ℹ️ {l}"))
                        elif 'time=' in line:
                            self.root.after(0, lambda l=line: self.log_message(f"⏱️ {l}"))
                        else:
                            self.root.after(0, lambda l=line: self.log_message(f"📋 {l}"))
            
            # Verificar resultado
            return_code = process.wait()
            
            if return_code == 0 and output_path.exists():
                file_size = output_path.stat().st_size / (1024 * 1024)  # MB
                self.root.after(0, lambda: self.log_message(f"📊 Archivo creado: {file_size:.2f} MB"))
                self.root.after(0, lambda: self.episode_progress.set(1.0))
                return True
            else:
                return False
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Error en conversión: {e}"))
            return False
    
    def _get_ffmpeg_command(self, ffmpeg_path, input_url, output_path):
        """Generar comando FFmpeg según configuración"""
        cmd = [ffmpeg_path, '-i', input_url]
        
        # Configurar video
        if self.compression_level.get() == "None":
            cmd.extend(['-c:v', 'copy'])
        else:
            cmd.extend(['-c:v', 'libx264'])
            
            # Configurar CRF según nivel de compresión
            crf_values = {
                "Low": "18",
                "Medium": "23",
                "High": "28",
                "Maximum": "35"
            }
            cmd.extend(['-crf', crf_values.get(self.compression_level.get(), "23")])
        
        # Configurar resolución
        if self.resolution.get() != "Original":
            resolution_map = {
                "1080p": "1920:1080",
                "720p": "1280:720",
                "480p": "854:480",
                "360p": "640:360"
            }
            cmd.extend(['-vf', f'scale={resolution_map[self.resolution.get()]}'])
        
        # Configurar audio
        if self.compression_level.get() == "None":
            cmd.extend(['-c:a', 'copy'])
        else:
            cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
        
        # Configuraciones adicionales
        cmd.extend(['-y', output_path])
        
        return cmd
    
    def stop_conversion(self):
        """Detener conversión"""
        self.is_converting = False
        self.log_message("⏹️ Conversión detenida por el usuario")
        
    def back_to_menu(self):
        """Volver al menú principal"""
        if self.is_converting:
            if messagebox.askyesno("Confirmar", "¿Detener la conversión y volver al menú?"):
                self.stop_conversion()
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Ejecutar la aplicación"""
        self.center_window()
        self.root.mainloop()