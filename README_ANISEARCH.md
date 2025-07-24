# Integración con AniSearch

Esta aplicación ahora incluye soporte para búsqueda de metadatos de anime usando la API de AniSearch.

## Configuración

### 1. Obtener credenciales OAuth de AniSearch

1. Ve a [AniSearch.es](https://www.anisearch.es/)
2. Crea una cuenta gratuita
3. Ve a tu panel de control > Apps
4. Registra una nueva aplicación OAuth
5. Obtén tu `client_id` y `client_secret`

### 2. Configurar credenciales

Edita el archivo `anisearch_config.py` y reemplaza:

```python
ANISEARCH_CLIENT_ID = 'TU_CLIENT_ID_AQUI'
ANISEARCH_CLIENT_SECRET = 'TU_CLIENT_SECRET_AQUI'
```

Con tus credenciales reales.

## Uso

### Búsqueda de Metadatos

1. En la sección "🔍 Búsqueda de Metadatos", selecciona la fuente:
   - **TMDB**: Para series de TV generales
   - **AniSearch**: Para anime

2. Ingresa el nombre del anime en el campo de búsqueda

3. Haz clic en "🔍 Buscar"

4. Selecciona el resultado correcto de la lista

5. Los campos se llenarán automáticamente:
   - Nombre de la serie
   - Año
   - ID de AniSearch (formato: `[anisearch-ID]`)

### Características de AniSearch

- **Búsqueda multiidioma**: Soporte para español, inglés, alemán, francés, italiano y japonés
- **Metadatos específicos de anime**: Información especializada para contenido de anime
- **Integración con OAuth**: Acceso seguro a la API de AniSearch
- **Resultados detallados**: Títulos en múltiples idiomas, años, descripciones

### URLs de la API de AniSearch

La aplicación utiliza las siguientes URLs base según el idioma:

- **Español**: https://www.anisearch.es
- **Inglés**: https://www.anisearch.com
- **Alemán**: https://www.anisearch.de
- **Francés**: https://www.anisearch.fr
- **Italiano**: https://www.anisearch.it
- **Japonés**: https://www.anisearch.jp

### Documentación de la API

Para más información sobre la API de AniSearch, consulta:

- [API de Ratings](https://api.anisearch.com/docs/api_ratings.html)
- [API de Usuario](https://api.anisearch.com/docs/api_user.html)
- [Guía OAuth](https://api.anisearch.com/docs/oauth_guide.html)

## Solución de Problemas

### Error: "Las bibliotecas necesarias para AniSearch no están disponibles"

Ejecuta:
```bash
pip install requests
```

### Error: "Por favor configura tus credenciales OAuth"

1. Verifica que el archivo `anisearch_config.py` existe
2. Asegúrate de haber reemplazado las credenciales de ejemplo
3. Verifica que las credenciales sean correctas

### Error de conexión

1. Verifica tu conexión a internet
2. Comprueba que AniSearch.com esté disponible
3. Verifica que tus credenciales OAuth sean válidas

## Notas Técnicas

- La aplicación utiliza la API base `https://api.anisearch.com`
- Los resultados se limitan a 10 elementos por búsqueda
- Se utiliza autenticación OAuth 2.0
- Los metadatos se almacenan en formato `[anisearch-ID]`
- Compatible con archivos .nfo para Jellyfin/Plex