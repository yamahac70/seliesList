# 📦 SeriesOrganizer - Ejecutable Windows

## ✅ Ejecutable Creado Exitosamente

Se ha generado el ejecutable `SeriesOrganizer.exe` usando PyInstaller.

### 📊 Información del Ejecutable

- **Archivo**: `dist/SeriesOrganizer.exe`
- **Tamaño**: ~194 MB (203,237,212 bytes)
- **Tipo**: Ejecutable único (onefile)
- **Interfaz**: Sin consola (windowed)
- **FFmpeg**: Incluido automáticamente

### 🚀 Cómo Usar

1. **Ejecutar directamente**: Haz doble clic en `SeriesOrganizer.exe`
2. **Desde línea de comandos**: `./dist/SeriesOrganizer.exe`
3. **Distribución**: Puedes copiar solo el archivo `.exe` a cualquier PC Windows

### 📁 Archivos Incluidos

- ✅ FFmpeg binarios (`bin/ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe`)
- ✅ Interfaz de usuario (`ui/` completa)
- ✅ Todas las dependencias de Python
- ✅ CustomTkinter y librerías necesarias

### 🎯 Funcionalidades

- **Organizador de Series**: Interfaz principal para organizar archivos de video
- **Convertidor de Series**: Herramienta para convertir M3U8 a MP4
- **Detección automática de FFmpeg**: Ya no necesitas instalar FFmpeg por separado
- **Interfaz moderna**: UI con CustomTkinter

### 📋 Requisitos del Sistema

- **SO**: Windows 10/11 (64-bit)
- **RAM**: Mínimo 4GB recomendado
- **Espacio**: ~200MB para el ejecutable
- **Permisos**: Puede requerir permisos de administrador para algunas operaciones

### 🔧 Comandos de Compilación Usados

```bash
# Instalación de PyInstaller
pip install pyinstaller

# Compilación del ejecutable
pyinstaller --onefile --windowed --add-data "bin;bin" --add-data "ui;ui" --name "SeriesOrganizer" app/main.py
```

### 📝 Notas Importantes

1. **Primera ejecución**: Puede tardar unos segundos en cargar
2. **Antivirus**: Algunos antivirus pueden marcar falsos positivos
3. **Actualizaciones**: Para nuevas versiones, recompila con PyInstaller
4. **Logs**: Los errores se mostrarán en ventanas de diálogo

### 🐛 Solución de Problemas

- **No abre**: Ejecuta desde cmd para ver errores
- **FFmpeg no detectado**: El ejecutable incluye FFmpeg automáticamente
- **Interfaz no aparece**: Verifica que no esté bloqueado por antivirus
- **Errores de permisos**: Ejecuta como administrador si es necesario

### 📦 Distribución

Puedes distribuir únicamente el archivo `SeriesOrganizer.exe` - no necesita instalación ni dependencias adicionales.