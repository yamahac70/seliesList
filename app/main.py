#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de Entrada Principal del Organizador de Series
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.config import get_config_manager
from app.controller import SeriesController
from ui.main_window import MainWindow
from ui.components.series_converter_window import SeriesConverterWindow

def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar gestor de configuración
        config_manager = get_config_manager()
        
        # Inicializar controlador
        controller = SeriesController(config_manager)
        
        # Mostrar menú principal
        show_main_menu(controller, config_manager)
        
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")
        sys.exit(1)

def show_main_menu(controller, config_manager):
    """Mostrar menú principal de selección"""
    import customtkinter as ctk
    from tkinter import messagebox
    
    # Configurar tema
    app_config = config_manager.get_app_config()
    ctk.set_appearance_mode(app_config.get("theme", "dark"))
    ctk.set_default_color_theme(app_config.get("color_theme", "blue"))
    
    # Crear ventana de menú
    menu_window = ctk.CTk()
    menu_window.title("📁 Organizador de Series - Menú Principal")
    menu_window.geometry("500x400")
    menu_window.resizable(False, False)
    
    # Centrar ventana
    menu_window.update_idletasks()
    x = (menu_window.winfo_screenwidth() // 2) - (menu_window.winfo_width() // 2)
    y = (menu_window.winfo_screenheight() // 2) - (menu_window.winfo_height() // 2)
    menu_window.geometry(f"+{x}+{y}")
    
    # Frame principal
    main_frame = ctk.CTkFrame(menu_window)
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Título
    title_label = ctk.CTkLabel(main_frame, 
                              text="📁 Organizador de Series",
                              font=ctk.CTkFont(size=28, weight="bold"))
    title_label.pack(pady=(30, 10))
    
    subtitle_label = ctk.CTkLabel(main_frame, 
                                 text="Selecciona una opción:",
                                 font=ctk.CTkFont(size=16))
    subtitle_label.pack(pady=(0, 40))
    
    def open_organizer():
        """Abrir organizador de series"""
        menu_window.destroy()
        app = MainWindow(controller, config_manager)
        app.root.mainloop()
    
    def open_converter():
        """Abrir convertidor de series"""
        menu_window.destroy()
        app = SeriesConverterWindow(controller, config_manager)
        app.root.mainloop()
    
    def show_about():
        """Mostrar información sobre la aplicación"""
        about_text = """
📁 Organizador de Series v2.0

🎯 Características:
• Organización automática de archivos de video
• Conversión de formatos de video
• Extracción de audio
• Integración con Jellyfin
• Búsqueda de metadatos (TMDB/Jikan)
• Estructura modular y extensible

👨‍💻 Desarrollado con Python y CustomTkinter
        """
        messagebox.showinfo("Acerca de", about_text)
    
    def exit_app():
        """Salir de la aplicación"""
        menu_window.destroy()
    
    # Botones del menú
    organizer_btn = ctk.CTkButton(main_frame, 
                                 text="🏷️ Organizador de Series",
                                 command=open_organizer,
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 height=50, width=300)
    organizer_btn.pack(pady=(0, 20))
    
    converter_btn = ctk.CTkButton(main_frame, 
                                 text="🔄 Convertidor de Series",
                                 command=open_converter,
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 height=50, width=300)
    converter_btn.pack(pady=(0, 20))
    
    about_btn = ctk.CTkButton(main_frame, 
                             text="ℹ️ Acerca de",
                             command=show_about,
                             font=ctk.CTkFont(size=14),
                             height=40, width=200)
    about_btn.pack(pady=(20, 10))
    
    exit_btn = ctk.CTkButton(main_frame, 
                            text="❌ Salir",
                            command=exit_app,
                            font=ctk.CTkFont(size=14),
                            height=40, width=200,
                            fg_color="#d32f2f",
                            hover_color="#b71c1c")
    exit_btn.pack(pady=(10, 0))
    
    # Ejecutar menú
    menu_window.mainloop()

if __name__ == "__main__":
    main()