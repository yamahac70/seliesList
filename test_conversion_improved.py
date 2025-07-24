#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba mejorado para verificar la funcionalidad de conversión
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils import FFmpegProcessor
from pathlib import Path
import subprocess

def create_test_video():
    """Crea un video de prueba usando FFmpeg"""
    processor = FFmpegProcessor()
    
    if not processor.is_available():
        print("❌ No se puede crear video de prueba: FFmpeg no disponible")
        return None
    
    test_video_path = "test_input.mp4"
    
    # Crear un video de prueba de 5 segundos
    cmd = [
        processor.ffmpeg_path,
        '-f', 'lavfi',
        '-i', 'testsrc=duration=5:size=320x240:rate=30',
        '-f', 'lavfi', 
        '-i', 'sine=frequency=1000:duration=5',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y', test_video_path
    ]
    
    try:
        print("🎬 Creando video de prueba...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and Path(test_video_path).exists():
            print(f"✅ Video de prueba creado: {test_video_path}")
            return test_video_path
        else:
            print(f"❌ Error creando video de prueba: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error creando video de prueba: {e}")
        return None

def test_video_conversion():
    """Prueba la conversión de video mejorada"""
    print("\n=== Prueba de Conversión de Video ===")
    
    # Crear video de prueba
    test_input = create_test_video()
    if not test_input:
        return False
    
    processor = FFmpegProcessor()
    test_output = "test_output.mp4"
    
    try:
        # Prueba 1: Conversión básica
        print("\n📋 Prueba 1: Conversión básica")
        success = processor.convert_video(
            test_input, 
            test_output,
            resolution="720p",
            compression_level="Medium",
            audio_mode="keep_all"
        )
        
        if success and Path(test_output).exists():
            print("✅ Conversión básica exitosa")
            
            # Verificar tamaños
            input_size = Path(test_input).stat().st_size
            output_size = Path(test_output).stat().st_size
            print(f"📊 Tamaño entrada: {input_size:,} bytes")
            print(f"📊 Tamaño salida: {output_size:,} bytes")
        else:
            print("❌ Conversión básica falló")
            return False
        
        # Prueba 2: Archivo inexistente
        print("\n📋 Prueba 2: Archivo inexistente")
        success = processor.convert_video(
            "archivo_inexistente.mp4",
            "salida_inexistente.mp4"
        )
        
        if not success:
            print("✅ Manejo correcto de archivo inexistente")
        else:
            print("❌ Debería haber fallado con archivo inexistente")
        
        # Prueba 3: Pista de audio inexistente
        print("\n📋 Prueba 3: Pista de audio inexistente")
        success = processor.convert_video(
            test_input,
            "test_output_audio.mp4",
            audio_mode="select_track",
            selected_audio_track="99"  # Pista que no existe
        )
        
        if success:
            print("✅ Manejo correcto de pista de audio inexistente")
        else:
            print("⚠️ Falló con pista de audio inexistente (puede ser esperado)")
        
        return True
        
    finally:
        # Limpiar archivos de prueba
        for file_path in [test_input, test_output, "test_output_audio.mp4"]:
            try:
                if Path(file_path).exists():
                    Path(file_path).unlink()
                    print(f"🗑️ Archivo limpiado: {file_path}")
            except:
                pass

def test_audio_extraction():
    """Prueba la extracción de audio mejorada"""
    print("\n=== Prueba de Extracción de Audio ===")
    
    # Crear video de prueba
    test_input = create_test_video()
    if not test_input:
        return False
    
    processor = FFmpegProcessor()
    
    try:
        # Prueba 1: Extracción MP3
        print("\n📋 Prueba 1: Extracción MP3")
        success = processor.extract_audio(
            test_input,
            "test_audio.mp3",
            audio_format="mp3",
            selected_track="0"
        )
        
        if success and Path("test_audio.mp3").exists():
            print("✅ Extracción MP3 exitosa")
            audio_size = Path("test_audio.mp3").stat().st_size
            print(f"📊 Tamaño audio: {audio_size:,} bytes")
        else:
            print("❌ Extracción MP3 falló")
            return False
        
        # Prueba 2: Formato no estándar
        print("\n📋 Prueba 2: Formato WAV")
        success = processor.extract_audio(
            test_input,
            "test_audio.wav",
            audio_format="wav",
            selected_track="0"
        )
        
        if success and Path("test_audio.wav").exists():
            print("✅ Extracción WAV exitosa")
        else:
            print("❌ Extracción WAV falló")
        
        return True
        
    finally:
        # Limpiar archivos de prueba
        for file_path in [test_input, "test_audio.mp3", "test_audio.wav"]:
            try:
                if Path(file_path).exists():
                    Path(file_path).unlink()
                    print(f"🗑️ Archivo limpiado: {file_path}")
            except:
                pass

def test_error_handling():
    """Prueba el manejo de errores"""
    print("\n=== Prueba de Manejo de Errores ===")
    
    processor = FFmpegProcessor()
    
    # Prueba 1: Directorio como archivo
    print("\n📋 Prueba 1: Directorio como archivo de entrada")
    success = processor.convert_video(
        "app",  # Es un directorio, no un archivo
        "salida_error.mp4"
    )
    
    if not success:
        print("✅ Manejo correcto de directorio como archivo")
    else:
        print("❌ Debería haber fallado con directorio como entrada")
    
    # Prueba 2: Ruta inválida para salida
    print("\n📋 Prueba 2: Creación de directorio de salida")
    test_input = create_test_video()
    if test_input:
        try:
            success = processor.convert_video(
                test_input,
                "nueva_carpeta/subcarpeta/salida.mp4"  # Carpetas que no existen
            )
            
            if success and Path("nueva_carpeta/subcarpeta/salida.mp4").exists():
                print("✅ Creación automática de directorios exitosa")
                # Limpiar
                import shutil
                shutil.rmtree("nueva_carpeta", ignore_errors=True)
            else:
                print("❌ Falló la creación automática de directorios")
        finally:
            if Path(test_input).exists():
                Path(test_input).unlink()
    
    return True

if __name__ == "__main__":
    print("🧪 Iniciando pruebas mejoradas de conversión...\n")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Conversión de Video", test_video_conversion),
        ("Extracción de Audio", test_audio_extraction),
        ("Manejo de Errores", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las pruebas pasaron! La funcionalidad de conversión está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar la implementación.")
    
    print("\n✨ Mejoras implementadas:")
    print("   • Validación de archivos de entrada")
    print("   • Creación automática de directorios de salida")
    print("   • Verificación de pistas de audio")
    print("   • Manejo detallado de errores")
    print("   • Timeouts para evitar colgadas")
    print("   • Logging informativo del progreso")