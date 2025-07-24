# 📁 SeList v1

Una aplicación completa para organizar, renombrar y convertir series de video con integración a Jellyfin y búsqueda automática de metadatos.

## M3U8 to MP4 Converter
### recomiendo usar la extencion cocoCut [COCOCUT](https://chromewebstore.google.com/detail/descargador-de-videos-coc/ekhbcipncbkfpkaianbjbcbmfehjflpf?hl=es)
Un sistema modular de conversión de archivos M3U8 a MP4 con interfaz gráfica moderna, desarrollado en Python usando Tkinter y FFmpeg.

## 🌟 Características Principales

### 🏠 Sistema Modular
- **Menú principal moderno** con interfaz CustomTkinter y diseño atractivo
- **Modo descarga única** para archivos individuales
- **Modo serie** para descargas masivas organizadas
- **Organizador de series** para archivos existentes
- **Interfaz moderna** con temas claro/oscuro y diseño intuitivo
- **Botones coloridos** con iconos y descripciones claras
- **Cambio de tema dinámico** entre modo claro y oscuro

### 📱 Modo Descarga Única
- **Conversión individual** de M3U8 a MP4 con audio incluido
- **Selección de resolución** (Original, 1080p, 720p, 480p, 360p)
- **Niveles de compresión** (None, Low, Medium, High, Maximum)
- **Barra de progreso determinística** con seguimiento en tiempo real
- **Log detallado en tiempo real** del proceso de FFmpeg

### 📺 Modo Serie
- **Lista de episodios** con URLs M3U8 y nombres personalizados
- **Organización automática** en carpetas por serie
- **Nomenclatura estructurada** (ej: "NombreSerie 01x01.mp4")
- **Conversión por lotes** con progreso individual y general
- **Gestión de listas** (cargar/guardar desde archivos)
- **Log categorizado** con emojis para mejor seguimiento

### 📁 Organizador de Series
- **Detección automática** de archivos de video en carpetas
- **Reordenamiento manual** de episodios con interfaz visual
- **Dos modos de operación**: solo renombrar o convertir y renombrar
- **Configuración flexible** de resolución y compresión
- **Nomenclatura consistente** con el modo serie
- **Gestión de archivos** (quitar, reordenar, previsualizar nombres)
- **Historial de directorios** para acceso rápido a carpetas frecuentes

### 🔧 Características Técnicas
- ⏹️ **Posibilidad de detener** la conversión en cualquier momento
- ✅ **Detección automática de FFmpeg** con indicador visual
- 🐍 **Entorno virtual de Python** para mejor gestión de dependencias
- 📁 **Información del archivo de salida** (tamaño, ubicación)

## 📋 Requisitos

- **Python 3.7+**
- **FFmpeg** (debe estar instalado y accesible desde PATH o en ubicaciones comunes)
- **Tkinter** (incluido con Python por defecto)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
git clone <url-del-repositorio>
cd proyectoEstructurado
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. FFmpeg (Incluido)

El proyecto ya incluye FFmpeg en el directorio `bin/` con los siguientes ejecutables:
- `ffmpeg.exe` - Convertidor principal
- `ffplay.exe` - Reproductor multimedia
- `ffprobe.exe` - Analizador de archivos multimedia

**Instalación alternativa (opcional):**

**Windows:**
- Descargar desde [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extraer y agregar al PATH del sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

## 🏗️ Arquitectura del Proyecto

Este proyecto utiliza una **arquitectura modular MVC (Model-View-Controller)** que proporciona:

- **📁 Separación clara de responsabilidades**: Cada componente tiene una función específica
- **🔧 Fácil mantenimiento**: Código organizado y escalable
- **🎨 Interfaz moderna**: Utiliza CustomTkinter para una UI atractiva
- **⚡ Rendimiento optimizado**: Ejecución eficiente con threading para operaciones pesadas

### Componentes principales:
- **`app/main.py`**: Punto de entrada de la aplicación
- **`app/controller.py`**: Lógica de control y coordinación
- **`app/model.py`**: Modelos de datos y lógica de negocio
- **`ui/main_window.py`**: Interfaz principal de usuario
- **`ui/components/`**: Componentes específicos de la UI

## 📖 Uso

### 🚀 Ejecución rápida

#### Menú Principal
```bash
python app/main.py
```
Este comando abre el menú principal moderno con interfaz CustomTkinter donde puedes elegir entre:
- **📱 Descarga Única** (Azul): Para convertir un solo archivo M3U8
- **📺 Modo Serie** (Verde): Para descargar múltiples episodios organizados
- **📁 Organizador de Series** (Naranja): Para ordenar y convertir archivos existentes

**Características del menú:**
- **🌓 Cambio de tema**: Alterna entre modo claro y oscuro
- **Diseño moderno**: Interfaz con esquinas redondeadas y colores atractivos
- **Botones grandes**: Fácil navegación con descripciones claras
- **Arquitectura modular**: Utiliza el patrón MVC para mejor organización del código

#### Ejecución desde el directorio del proyecto
```bash
cd proyectoEstructurado
python app/main.py
```

### 📱 Modo Descarga Única

1. **Ejecutar el programa**
   - Ejecutar `python app/main.py` y seleccionar "Descarga Única"

2. **Configurar la entrada**
   - Pegar la URL del archivo M3U8 en el campo "URL M3U8"
   - Seleccionar o escribir la ruta de salida para el archivo MP4

3. **Configurar opciones de video**
   - **Resolución**: Elegir entre Original, 1080p, 720p, 480p, 360p
   - **Compresión**: Seleccionar nivel (None, Low, Medium, High, Maximum)

4. **Iniciar conversión**
   - Hacer clic en "🚀 Iniciar Conversión"
   - Observar el progreso en tiempo real con log detallado de FFmpeg

### 📺 Modo Serie

1. **Configurar serie**
   - Ingresar el nombre de la serie
   - Especificar el número de temporada (ej: "01")
   - Elegir el episodio inicial (ej: "01" para empezar desde el primer episodio, "05" para empezar desde el quinto)
   - Seleccionar carpeta destino usando el botón "📁 Seleccionar ▼" (donde se guardará la carpeta de la serie)
     - Al hacer clic, muestra un menú con los últimos 5 directorios utilizados
     - Opción "📁 Seleccionar nueva carpeta..." para explorar nuevas ubicaciones
     - Historial guardado automáticamente en `directory_history.json`

2. **Agregar episodios**
   - Pegar URL M3U8 del episodio
   - Escribir nombre del episodio (opcional)
   - Hacer clic en "➕ Agregar"
   - Repetir para todos los episodios

3. **Gestión de episodios**
   - **Editar números**: Haz doble clic en el número de episodio o usa el botón "✏️ Editar Nº"
   - **Reordenar**: Usa los botones "🔼 Subir" y "🔽 Bajar" para cambiar el orden
   - **Eliminar**: Selecciona un episodio y usa "🗑️ Eliminar"

4. **Gestión de lista**
   - **📁 Cargar Lista**: Importar desde archivo de texto
   - **💾 Guardar Lista**: Exportar lista actual
   - **🗑️ Eliminar**: Quitar episodio seleccionado
   - **🔄 Limpiar Todo**: Vaciar lista completa

5. **Configurar video**
   - Seleccionar resolución y compresión (igual que modo único)

6. **Iniciar conversión**
   - Hacer clic en "🚀 Iniciar Conversión"
   - Ver progreso general y por episodio
   - Los archivos se guardan como: `NombreSerie 01x01.mp4`

### 📁 Organizador de Series

Este modo permite organizar archivos de video existentes en tu computadora, reordenarlos y opcionalmente convertirlos.

1. **Configurar carpetas**
   - **Carpeta origen**: Usar "📁 Seleccionar ▼" para elegir la carpeta que contiene los archivos de video
     - Muestra historial de las últimas 5 carpetas utilizadas
     - Opción para seleccionar nueva carpeta
   - **Carpeta destino**: Seleccionar donde se guardarán los archivos organizados
   - Hacer clic en "🔍 Detectar" para buscar archivos de video automáticamente

2. **Configurar serie**
   - Ingresar el **nombre de la serie**
   - Especificar **temporada** (ej: "01")
   - Definir **episodio inicial** (ej: "01" para empezar desde el primer episodio)

3. **Seleccionar modo de operación**
   - **📝 Solo renombrar archivos**: Copia los archivos con nuevos nombres organizados
   - **🔄 Convertir y renombrar**: Convierte los archivos y los renombra (requiere FFmpeg)
     - **Resolución**: Original, 1080p, 720p, 480p, 360p
     - **Compresión**: None, Low, Medium, High, Maximum

4. **Gestión de archivos detectados**
   - **Vista previa**: La lista muestra el orden actual, nombre original, nuevo nombre y tamaño
   - **Reordenar**: Usar "🔼 Subir" y "🔽 Bajar" para cambiar el orden de episodios
   - **Actualizar**: "🔄 Actualizar Nombres" para ver los cambios en la nomenclatura
   - **Quitar**: "🗑️ Quitar" para remover archivos de la lista (no los elimina del disco)

5. **Procesamiento**
   - Hacer clic en "🚀 Iniciar Procesamiento"
   - Monitorear progreso general y por archivo
   - Los archivos se organizan como: `[CarpetaDestino]/[NombreSerie]/NombreSerie 01x01.mp4`

#### Formatos de video soportados:
- MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, MPG, MPEG

### 📄 Formato de archivo de lista

Para cargar listas de episodios, usa este formato en un archivo `.txt`:
```
# Lista de episodios - Formato: URL|Nombre
https://ejemplo.com/episodio1.m3u8|Episodio 1: Piloto
https://ejemplo.com/episodio2.m3u8|Episodio 2: El comienzo
https://ejemplo.com/episodio3.m3u8|Episodio 3: La revelación
```

### ⚙️ Opciones Avanzadas

#### Configuración de video:
- **Resolución:** Selecciona la resolución de salida deseada (Original mantiene la resolución original)
- **Compresión:** Elige el nivel de compresión:
  - **Sin compresión:** Copia directa (más rápido, mayor tamaño)
  - **Baja:** Máxima calidad con compresión mínima
  - **Medio:** Balance entre calidad y tamaño
  - **Alta:** Menor tamaño con buena calidad
  - **Máxima:** Mínimo tamaño (puede afectar la calidad)

#### Monitoreo del progreso:
- Observa la barra de progreso con porcentaje en tiempo real
- Ve el tiempo transcurrido vs tiempo total
- Revisa el log detallado del proceso

#### Control de conversión:
- Usa el botón "⏹️ Detener" para cancelar la conversión en cualquier momento

## 📁 Estructura del Proyecto

```
proyectoEstructurado/
│
├── app/                       # Aplicación principal
│   ├── __init__.py           # Inicializador del módulo
│   ├── main.py               # Punto de entrada de la aplicación
│   ├── controller.py         # Controlador principal (MVC)
│   ├── model.py              # Modelo de datos y lógica de negocio
│   ├── utils.py              # Utilidades y funciones auxiliares
│   └── config.py             # Configuración de la aplicación
│
├── ui/                       # Interfaz de usuario
│   ├── __init__.py           # Inicializador del módulo UI
│   ├── main_window.py        # Ventana principal de la aplicación
│   ├── components/           # Componentes de la interfaz
│   │   ├── __init__.py
│   │   └── series_converter_window.py  # Ventana del convertidor de series
│   └── assets/               # Recursos gráficos (iconos, imágenes)
│
├── bin/                      # Ejecutables de FFmpeg
│   ├── ffmpeg.exe           # Ejecutable principal de FFmpeg
│   ├── ffplay.exe           # Reproductor de FFmpeg
│   └── ffprobe.exe          # Analizador de medios
│
├── data/                     # Datos de la aplicación
│   └── (archivos de configuración y datos)
│
├── tests/                    # Pruebas unitarias
│   └── __init__.py
│
├── util/                     # Utilidades adicionales
│
├── dist/                     # Ejecutable compilado (generado por PyInstaller)
│   └── SeriesOrganizer.exe   # Ejecutable final de la aplicación
│
├── requirements.txt          # Dependencias de Python
├── SeriesOrganizer.spec      # Configuración de PyInstaller
├── README.md                 # Documentación principal
├── README_EJECUTABLE.md      # Documentación del ejecutable
├── README_ANISEARCH.md       # Documentación de la API AniSearch
├── README_JIKAN.md           # Documentación de la API Jikan
└── .gitignore               # Archivos ignorados por Git

**Nota**: Esta es la estructura del proyecto modularizado y organizado según las mejores prácticas de desarrollo.
```

## Funcionalidades Técnicas

- **Detección automática de FFmpeg:** El programa busca FFmpeg en el directorio local o en PATH
- **Conversión inteligente:** 
  - Modo "Sin compresión": Usa `-c copy` para copia directa (más rápido)
  - Modos con compresión: Usa `libx264` con diferentes niveles CRF
- **Escalado de resolución:** Implementa filtros de escala para cambiar resolución
- **Configuración de calidad:** Ajusta CRF y presets según el nivel de compresión seleccionado
- **Progreso en tiempo real:** Parsea la salida de FFmpeg para mostrar progreso preciso
- **Compatibilidad de audio:** Incluye filtro `aac_adtstoasc` para compatibilidad con contenedores MP4
- **Interfaz responsiva:** La conversión se ejecuta en un hilo separado para mantener la UI responsiva
- **Manejo de errores:** Captura y muestra errores de manera comprensible con emojis
- **Información detallada:** Muestra duración, tiempo transcurrido y tamaño del archivo final

## Solución de Problemas

### FFmpeg no encontrado
- Verifica que el directorio `bin/` contenga `ffmpeg.exe`
- O asegúrate de que FFmpeg esté instalado en tu sistema y disponible en PATH
- El programa detecta automáticamente FFmpeg en `bin/ffmpeg.exe` o en el PATH del sistema

### Error de conversión
- Verifica que la URL M3U8 sea válida y accesible
- Asegúrate de tener permisos de escritura en el directorio de salida
- Revisa el log para obtener detalles específicos del error

### Problemas de red
- Verifica tu conexión a internet
- Algunas URLs M3U8 pueden requerir headers específicos o autenticación

## Comandos FFmpeg Utilizados

### Modo Sin Compresión (más rápido):
```bash
ffmpeg -i [URL_M3U8] -c copy -y -progress pipe:1 [ARCHIVO_SALIDA]
```

### Modo Con Compresión:
```bash
ffmpeg -i [URL_M3U8] -vf scale=[RESOLUCION] -c:v libx264 -crf [CALIDAD] -preset [VELOCIDAD] -c:a aac -b:a 128k -bsf:a aac_adtstoasc -y -progress pipe:1 [ARCHIVO_SALIDA]
```

### Parámetros explicados:
- `-i [URL_M3U8]`: Archivo de entrada (URL del M3U8)
- `-vf scale=[RESOLUCION]`: Escala el video a la resolución especificada
- `-c:v libx264`: Codec de video H.264
- `-crf [CALIDAD]`: Factor de calidad constante (18=alta, 23=media, 28=baja, 32=mínima)
- `-preset [VELOCIDAD]`: Velocidad de codificación (slow, medium, fast, veryfast)
- `-c:a aac`: Codec de audio AAC
- `-b:a 128k`: Bitrate de audio 128 kbps
- `-bsf:a aac_adtstoasc`: Convierte AAC ADTS a ASC para compatibilidad MP4
- `-y`: Sobrescribe el archivo de salida si existe
- `-progress pipe:1`: Envía información de progreso para la barra de progreso
- `[ARCHIVO_SALIDA]`: Ruta del archivo MP4 de salida

## 📄 Licencia y Términos de Uso

### 🚫 Uso No Comercial
Este proyecto está destinado **exclusivamente para uso personal, educativo y de investigación**. Queda **estrictamente prohibido**:

- ❌ **Uso comercial** o con fines de lucro
- ❌ **Venta o distribución comercial** del software o sus derivados
- ❌ **Uso en servicios comerciales** o aplicaciones de pago
- ❌ **Redistribución con fines comerciales**

### ✅ Usos Permitidos
- ✅ **Uso personal** para organizar tu propia colección de series
- ✅ **Fines educativos** y de aprendizaje
- ✅ **Investigación** y desarrollo no comercial
- ✅ **Modificación y mejora** del código para uso personal

### ⚖️ Responsabilidad Legal
- El usuario es **completamente responsable** del uso que haga de este software
- Asegúrate de cumplir con las **leyes de derechos de autor** de tu país
- Respeta los **términos de servicio** de las plataformas de streaming
- Este software no debe usarse para **piratería** o **violación de derechos de autor**

### 📝 Disclaimer
Este proyecto se proporciona "tal como está", sin garantías de ningún tipo. Los desarrolladores no se hacen responsables del uso indebido del software o de cualquier consecuencia legal derivada de su uso.

---

**© 2024 - Organizador de Series v2.0**  
*Proyecto de código abierto para uso personal y educativo únicamente*