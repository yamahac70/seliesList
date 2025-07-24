#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las mejoras en el logging y progreso
de la funcionalidad de conversión de video.
"""

import os
import sys
import tempfile
from pathlib import Path

# Agregar el directorio app al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Importar directamente desde app
from app.utils import FFmpegProcessor
from app.controller import SeriesController
from app.model import SeriesModel

def create_test_video(output_path: str, duration: int = 10) -> bool:
    """Crea un video de prueba usando FFmpeg"""
    ffmpeg = FFmpegProcessor()
    if not ffmpeg.is_available():
        print("❌ FFmpeg no disponible para crear video de prueba")
        return False
    
    cmd = [
        ffmpeg.ffmpeg_path,
        '-f', 'lavfi',
        '-i', f'testsrc=duration={duration}:size=320x240:rate=1',
        '-f', 'lavfi', 
        '-i', 'sine=frequency=1000:duration=10',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y', output_path
    ]
    
    try:
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error creando video de prueba: {e}")
        return False

def test_controller_logging():
    """Prueba el logging mejorado del controlador"""
    print("\n🧪 Probando logging mejorado del controlador...")
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear video de prueba
        test_video = temp_path / "test_video.mp4"
        print(f"📹 Creando video de prueba: {test_video}")
        
        if not create_test_video(str(test_video)):
            print("❌ No se pudo crear video de prueba")
            return False
        
        # Configurar modelo y controlador
        model = SeriesModel()
        controller = SeriesController(model)
        
        # Agregar archivo al modelo usando detect_video_files
        model.detect_video_files(str(temp_path))
        model.metadata.name = "Serie de Prueba"
        
        # Directorio de salida
        output_dir = temp_path / "output"
        
        print("\n🎬 Iniciando conversión con logging mejorado...")
        
        # Configurar callback para capturar logs
        logs = []
        def capture_log(message):
            logs.append(message)
            print(f"📝 LOG: {message}")
        
        controller.log_message = capture_log
        
        # Iniciar procesamiento
        controller.start_processing(
            operation_mode="convert",
            output_directory=str(output_dir),
            resolution="320x240",
            compression_level="medium",
            audio_mode="keep_all",
            selected_audio_track="0",
            audio_format="mp3",
            jellyfin_structure=False,
            create_nfo=False
        )
        
        # Esperar a que termine
        import time
        while controller.is_processing:
            time.sleep(0.5)
        
        print("\n📊 Resumen de logs capturados:")
        for i, log in enumerate(logs, 1):
            print(f"  {i}. {log}")
        
        # Verificar que se generaron los logs esperados
        expected_logs = [
            "📁 Directorio de salida:",
            "🎯 Modo de operación:",
            "🎬 Convirtiendo:",
            "⚙️ Configuración:",
            "✅ Convertido:",
            "📂 Archivos guardados en:",
            "📊 Total procesados:"
        ]
        
        found_logs = []
        for expected in expected_logs:
            for log in logs:
                if expected in log:
                    found_logs.append(expected)
                    break
        
        print(f"\n✅ Logs encontrados: {len(found_logs)}/{len(expected_logs)}")
        for log in found_logs:
            print(f"  ✓ {log}")
        
        missing_logs = set(expected_logs) - set(found_logs)
        if missing_logs:
            print("❌ Logs faltantes:")
            for log in missing_logs:
                print(f"  ✗ {log}")
        
        # Verificar que se creó el archivo de salida
        output_files = list(output_dir.rglob("*.mp4"))
        if output_files:
            print(f"\n✅ Archivo de salida creado: {output_files[0]}")
            return True
        else:
            print("\n❌ No se encontró archivo de salida")
            return False

def test_ffmpeg_progress():
    """Prueba el progreso en tiempo real de FFmpeg"""
    print("\n🧪 Probando progreso en tiempo real de FFmpeg...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear video de prueba más largo para ver progreso
        test_video = temp_path / "test_video_long.mp4"
        print(f"📹 Creando video de prueba largo: {test_video}")
        
        if not create_test_video(str(test_video), duration=30):  # 30 segundos
            print("❌ No se pudo crear video de prueba")
            return False
        
        # Probar conversión directa
        ffmpeg = FFmpegProcessor()
        output_file = temp_path / "converted.mp4"
        
        print("\n🎬 Iniciando conversión con progreso...")
        success = ffmpeg.convert_video(
            str(test_video),
            str(output_file),
            resolution="480p",
            compression_level="Medium",
            audio_mode="keep_all"
        )
        
        if success:
            print(f"\n✅ Conversión exitosa: {output_file}")
            return True
        else:
            print("\n❌ Error en conversión")
            return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de mejoras en logging y progreso")
    print("=" * 60)
    
    # Verificar FFmpeg
    ffmpeg = FFmpegProcessor()
    if not ffmpeg.is_available():
        print("❌ FFmpeg no está disponible. No se pueden ejecutar las pruebas.")
        return False
    
    print(f"✅ FFmpeg encontrado: {ffmpeg.ffmpeg_path}")
    
    # Ejecutar pruebas
    tests = [
        ("Logging del controlador", test_controller_logging),
        ("Progreso de FFmpeg", test_ffmpeg_progress)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en prueba '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las mejoras funcionan correctamente!")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar implementación.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)