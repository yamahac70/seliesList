# Integración con Jikan API (MyAnimeList)

Esta aplicación ahora incluye soporte para búsqueda de metadatos de anime usando la **Jikan API**, que es una API no oficial de MyAnimeList más confiable y estable que AniSearch.

## ¿Qué es Jikan?

**Jikan** es una API REST no oficial de MyAnimeList que proporciona:
- ✅ **Acceso gratuito** sin necesidad de API keys
- ✅ **Alta disponibilidad** y confiabilidad
- ✅ **Datos completos** de anime y manga
- ✅ **Rate limiting** automático respetando los límites
- ✅ **Soporte multiidioma** (aunque los datos están principalmente en inglés/japonés)

## Características de la Integración

### 🔍 Búsqueda de Anime
- Búsqueda por título en múltiples idiomas
- Resultados ordenados por popularidad
- Información detallada incluyendo:
  - Título original y en inglés
  - Año de emisión
  - Descripción/sinopsis
  - Géneros
  - Rating/puntuación
  - Imagen de portada
  - URL de MyAnimeList

### 📋 Metadatos Disponibles
- **ID de MyAnimeList** (formato: `[jikan-ID]`)
- **Títulos múltiples**: Original, inglés, japonés
- **Información temporal**: Año de emisión
- **Clasificación**: Rating de la comunidad
- **Géneros**: Lista completa de géneros
- **Descripción**: Sinopsis oficial

### ⚡ Funciones Principales

1. **Búsqueda Básica**:
   ```python
   from jikan_api import JikanAPI
   
   api = JikanAPI()
   results = api.search_anime("Naruto", limit=10)
   ```

2. **Búsqueda Rápida**:
   ```python
   from jikan_api import search_anime_quick
   
   result = search_anime_quick("One Piece")
   ```

3. **Detalles Completos**:
   ```python
   details = api.get_anime_details("20")  # ID de Naruto
   ```

## Ventajas sobre AniSearch

| Característica | Jikan (MyAnimeList) | AniSearch |
|---|---|---|
| **Disponibilidad** | ✅ Alta (99%+) | ❌ Intermitente |
| **API Key** | ✅ No requerida | ❌ Requerida |
| **Rate Limiting** | ✅ Automático | ⚠️ Manual |
| **Datos** | ✅ Completos | ⚠️ Limitados |
| **Estabilidad** | ✅ Muy estable | ❌ Inestable |
| **Documentación** | ✅ Excelente | ⚠️ Limitada |
| **Comunidad** | ✅ Grande | ⚠️ Pequeña |

## Configuración

### Instalación de Dependencias
```bash
pip install requests
```

### Uso en la Aplicación
1. Abre el **Organizador de Series**
2. En la sección "Búsqueda de Metadatos", selecciona **"Jikan (MyAnimeList)"**
3. Ingresa el nombre del anime a buscar
4. Haz clic en **"🔍 Buscar"**
5. Selecciona el resultado correcto de la lista
6. Los metadatos se aplicarán automáticamente

## Rate Limiting

La API de Jikan tiene los siguientes límites:
- **3 requests por segundo**
- **60 requests por minuto**

La implementación incluye **rate limiting automático** para respetar estos límites y evitar errores.

## Estructura de Datos

```python
@dataclass
class AnimeResult:
    id: str                    # ID de MyAnimeList
    title: str                 # Título principal
    title_english: str         # Título en inglés
    title_japanese: str        # Título en japonés
    title_romaji: str          # Título en romaji (no disponible en Jikan)
    year: str                  # Año de emisión
    overview: str              # Sinopsis/descripción
    rating: float              # Puntuación (0-10)
    image_url: str             # URL de la imagen de portada
    genres: List[str]          # Lista de géneros
    url: str                   # URL de MyAnimeList
```

## URLs y Referencias

- **Jikan API**: https://jikan.moe/
- **Documentación**: https://docs.api.jikan.moe/
- **MyAnimeList**: https://myanimelist.net/
- **GitHub**: https://github.com/jikan-me/jikan

## Ejemplos de Uso

### Búsqueda Simple
```python
from jikan_api import JikanAPI

api = JikanAPI()
results = api.search_anime("Attack on Titan")

for result in results:
    print(f"{result.title} ({result.year}) - Rating: {result.rating}/10")
```

### Obtener Detalles
```python
# Buscar y obtener detalles del primer resultado
results = api.search_anime("Death Note")
if results:
    details = api.get_anime_details(results[0].id)
    print(f"Descripción: {details.overview}")
    print(f"Géneros: {', '.join(details.genres)}")
```

## Solución de Problemas

### Error: "Las bibliotecas necesarias para Jikan no están disponibles"
**Solución:**
1. Instala requests: `pip install requests`
2. Verifica que `jikan_api.py` esté en el directorio del proyecto
3. Reinicia la aplicación

### Error: "Rate limit exceeded"
**Solución:**
- La aplicación maneja automáticamente el rate limiting
- Si persiste, espera unos segundos entre búsquedas

### Error: "No se encontraron resultados"
**Solución:**
1. Verifica la ortografía del nombre del anime
2. Prueba con el título en inglés
3. Usa términos más generales (ej: "Naruto" en lugar de "Naruto Shippuden")

### Error de conectividad
**Solución:**
1. Verifica tu conexión a internet
2. Comprueba que https://api.jikan.moe esté disponible
3. Intenta nuevamente después de unos minutos

## Migración desde AniSearch

Si anteriormente usabas AniSearch:

1. **IDs de metadatos**: Los IDs cambiarán de `[anisearch-ID]` a `[jikan-ID]`
2. **Búsquedas**: El proceso es idéntico, solo cambia la fuente
3. **Datos**: Jikan proporciona más información y es más confiable
4. **Sin configuración**: No necesitas API keys ni configuración adicional

## Notas Importantes

- ⚠️ **Idioma**: Los datos están principalmente en inglés y japonés
- ⚠️ **Cobertura**: Enfocado en anime/manga, no series de TV occidentales
- ✅ **Gratuito**: Completamente gratuito sin límites de uso razonables
- ✅ **Actualizado**: Datos sincronizados con MyAnimeList regularmente

---

*Esta integración reemplaza completamente a AniSearch para proporcionar una experiencia más confiable y estable en la búsqueda de metadatos de anime.*