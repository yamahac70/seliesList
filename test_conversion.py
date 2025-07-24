#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la funcionalidad de conversión
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils import FFmpegProcessor
from pathlib import Path

def test_ffmpeg_functionality():
    """Prueba la funcionalidad básica de FFmpeg"""
    print("=== Prueba de Funcionalidad FFmpeg ===")
    
    # Crear instancia del procesador
    processor = FFmpegProcessor()
    
    print(f"FFmpeg disponible: {processor.is_available()}")
    print(f"Ruta de FFmpeg: {processor.ffmpeg_path}")
    
    if not processor.is_available():
        print("❌ FFmpeg no está disponible")
        return False
    
    # Probar comando básico de FFmpeg
    import subprocess
    try:
        result = subprocess.run([processor.ffmpeg_path, '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg responde correctamente")
            print(f"Versión: {result.stdout.split()[2] if len(result.stdout.split()) > 2 else 'Desconocida'}")
        else:
            print("❌ FFmpeg no responde correctamente")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando FFmpeg: {e}")
        return False
    
    # Verificar codecs disponibles
    try:
        result = subprocess.run([processor.ffmpeg_path, '-codecs'], 
                              capture_output=True, text=True, timeout=10)
        if 'libx264' in result.stdout:
            print("✅ Codec libx264 disponible")
        else:
            print("⚠️ Codec libx264 no encontrado")
            
        if 'libmp3lame' in result.stdout:
            print("✅ Codec libmp3lame disponible")
        else:
            print("⚠️ Codec libmp3lame no encontrado")
            
    except Exception as e:
        print(f"⚠️ No se pudo verificar codecs: {e}")
    
    return True

def analyze_conversion_issues():
    """Analiza posibles problemas en el código de conversión"""
    print("\n=== Análisis de Problemas Potenciales ===")
    
    issues = []
    
    # Problema 1: Manejo de errores limitado
    issues.append({
        'problema': 'Manejo de errores limitado',
        'descripcion': 'El método convert_video solo retorna True/False sin detalles del error',
        'solucion': 'Agregar logging detallado y captura de stderr de FFmpeg'
    })
    
    # Problema 2: Falta de validación de archivos
    issues.append({
        'problema': 'Falta validación de archivos',
        'descripcion': 'No se verifica si el archivo de entrada existe o es válido',
        'solucion': 'Agregar validación de archivos de entrada antes de la conversión'
    })
    
    # Problema 3: Configuración de audio incompleta
    issues.append({
        'problema': 'Configuración de audio incompleta',
        'descripcion': 'El mapeo de audio puede fallar si no existe la pista especificada',
        'solucion': 'Verificar pistas de audio disponibles antes del mapeo'
    })
    
    # Problema 4: Falta de progreso en tiempo real
    issues.append({
        'problema': 'Sin progreso en tiempo real',
        'descripcion': 'No hay feedback del progreso durante la conversión',
        'solucion': 'Implementar callback de progreso usando -progress de FFmpeg'
    })
    
    # Problema 5: Timeout no configurado
    issues.append({
        'problema': 'Sin timeout en conversiones',
        'descripcion': 'Las conversiones pueden colgarse indefinidamente',
        'solucion': 'Agregar timeout apropiado para conversiones largas'
    })
    
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {issue['problema']}")
        print(f"   Descripción: {issue['descripcion']}")
        print(f"   Solución: {issue['solucion']}")
    
    return issues

if __name__ == "__main__":
    print("Iniciando pruebas de conversión...\n")
    
    # Probar funcionalidad básica
    ffmpeg_ok = test_ffmpeg_functionality()
    
    # Analizar problemas
    issues = analyze_conversion_issues()
    
    print(f"\n=== Resumen ===")
    print(f"FFmpeg funcional: {'✅ Sí' if ffmpeg_ok else '❌ No'}")
    print(f"Problemas identificados: {len(issues)}")
    
    if ffmpeg_ok:
        print("\n✅ FFmpeg está correctamente configurado")
        print("⚠️ Sin embargo, hay problemas en la implementación que pueden causar fallos")
    else:
        print("\n❌ FFmpeg no está funcionando correctamente")
    
    print("\nRecomendación: Revisar y mejorar el manejo de errores en la conversión")