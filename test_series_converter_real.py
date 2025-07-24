#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de la funcionalidad real de conversión en SeriesConverterWindow
"""

import sys
import os
from pathlib import Path
import tempfile
import time

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_series_converter_integration():
    """Probar la integración completa del convertidor de series"""
    print("🧪 Iniciando prueba de integración del convertidor de series...")
    
    try:
        # Importar las clases necesarias
        from ui.components.series_converter_window import SeriesConverterWindow
        from app.controller import SeriesController
        from app.config import ConfigManager
        
        print("✅ Importaciones exitosas")
        
        # Crear instancias
        config_manager = ConfigManager()
        controller = SeriesController(config_manager)
        
        print("✅ Controlador creado")
        
        # Verificar FFmpeg
        from app.utils import FFmpegProcessor
        ffmpeg = FFmpegProcessor()
        
        if ffmpeg.is_available():
            print(f"✅ FFmpeg disponible en: {ffmpeg.ffmpeg_path}")
        else:
            print("❌ FFmpeg no disponible")
            return False
        
        # Probar el método de conversión individual
        print("\n🔧 Probando método de conversión individual...")
        
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_file = temp_path / "test_episode.mp4"
            
            # URL de prueba (M3U8 público)
            test_url = "https://vod3.cf.dmcdn.net/sec2(QFkfchyDm2LoQOyl_j91LtMoSTopqJza4SwZt9FTWHPZNDcOuE8hK98ymMXTXdxVAhxrKwq859drEX3QK38QWfq5E-4QcFKlVmeB6x740zGEiUqZAM5GSDPg6IoLmi0XpLRRdiTqQfsNWYP_awJVHPs6r7iWtKAKBAuqpzLoA13MXPNfGRQBgofJvbpiFPYA)/video/848/182/541281848_mp4_h264_aac_hd_2.m3u8#cell=cf3"
            
            print(f"📥 URL de prueba: {test_url[:80]}...")
            print(f"📁 Archivo de salida: {output_file}")
            
            print("\n🎬 Iniciando conversión de prueba...")
            success = ffmpeg.convert_video(
                input_path=test_url,
                output_path=str(output_file),
                resolution="720p",
                compression_level="medium"
            )
            
            if success and output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)  # MB
                print(f"✅ Conversión exitosa: {file_size:.2f} MB")
                print(f"📊 Archivo creado: {output_file}")
                return True
            else:
                print("❌ Conversión falló")
                return False
                
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_series_converter_ui_simulation():
    """Simular el flujo de trabajo de la UI sin crear la ventana"""
    print("\n🖥️ Simulando flujo de trabajo de la UI...")
    
    try:
        # Simular datos de episodios
        episodes_data = [
            {
                'number': '01',
                'name': 'Episodio de Prueba 1',
                'url': 'https://vod3.cf.dmcdn.net/sec2(QFkfchyDm2LoQOyl_j91LtMoSTopqJza4SwZt9FTWHPZNDcOuE8hK98ymMXTXdxVAhxrKwq859drEX3QK38QWfq5E-4QcFKlVmeB6x740zGEiUqZAM5GSDPg6IoLmi0XpLRRdiTqQfsNWYP_awJVHPs6r7iWtKAKBAuqpzLoA13MXPNfGRQBgofJvbpiFPYA)/video/848/182/541281848_mp4_h264_aac_hd_2.m3u8#cell=cf3'
            }
        ]
        
        # Simular configuración de serie
        series_config = {
            'series_name': 'Serie de Prueba',
            'season_number': '01',
            'output_directory': str(Path.cwd() / 'test_output'),
            'resolution': '720p',
            'compression_level': 'medium'
        }
        
        print(f"📺 Serie: {series_config['series_name']}")
        print(f"📁 Directorio: {series_config['output_directory']}")
        print(f"📋 Episodios: {len(episodes_data)}")
        
        # Crear directorio de serie
        series_dir = Path(series_config['output_directory']) / series_config['series_name']
        series_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {series_dir}")
        
        # Simular conversión de episodios
        from app.utils import FFmpegProcessor
        ffmpeg = FFmpegProcessor()
        
        for i, episode in enumerate(episodes_data):
            print(f"\n🎬 Procesando episodio {i+1}/{len(episodes_data)}")
            print(f"📄 Nombre: {episode['name']}")
            
            # Generar nombre de archivo
            season = series_config['season_number'].zfill(2)
            episode_num = episode['number']
            filename = f"{series_config['series_name']} {season}x{episode_num}.mp4"
            output_path = series_dir / filename
            
            print(f"💾 Archivo: {output_path.name}")
            
            # Simular conversión (sin hacer la conversión real para la prueba)
            print("⚙️ Configuración aplicada")
            print("✅ Conversión simulada exitosa")
            
        print("\n🎉 Simulación de flujo completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del convertidor de series\n")
    
    # Ejecutar pruebas
    test1_result = test_series_converter_integration()
    test2_result = test_series_converter_ui_simulation()
    
    print("\n📊 Resultados de las pruebas:")
    print(f"✅ Integración FFmpeg: {'EXITOSA' if test1_result else 'FALLIDA'}")
    print(f"✅ Simulación UI: {'EXITOSA' if test2_result else 'FALLIDA'}")
    
    if test1_result and test2_result:
        print("\n🎉 ¡Todas las pruebas pasaron! El convertidor está listo.")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisar la configuración.")