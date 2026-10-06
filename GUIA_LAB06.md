# Laboratorio 06 - Motor de plantillas con Django

## Puesta en marcha

Desde PowerShell, en la carpeta del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news_demo
python manage.py runserver 8001
```

- Portal: `http://127.0.0.1:8001/noticias/`
- Administrador: `http://127.0.0.1:8001/admin/`
- Biblioteca de los laboratorios anteriores: `http://127.0.0.1:8001/`

`seed_news_demo` crea tres autores, tres categorías y seis noticias con imágenes de demostración. Se puede ejecutar más de una vez sin duplicar las noticias.

## Estructura implementada

```text
config/
news/
  admin.py
  models.py
  urls.py
  views.py
  templates/news/
    _article_card.html
    article_detail.html
    category_articles.html
    home.html
static/news/css/portal.css
```

- `templates/base.html` contiene los bloques `title`, `content` y `sidebar`.
- `_article_card.html` se incluye tanto en la portada como en el listado por categoría.
- Las URLs tienen nombre propio y las plantillas usan `{% url %}` para enlazarse.
- Las imágenes destacadas se guardan en `media/articles/` y se sirven solo en desarrollo.

## Capturas para el entregable

1. Explorador de VS Code con `config`, `news`, `static`, `templates` y `manage.py`.
2. `config/settings.py` mostrando `news.apps.NewsConfig` en `INSTALLED_APPS`, `DIRS`, `STATIC_URL`, `STATICFILES_DIRS`, `MEDIA_URL` y `MEDIA_ROOT`.
3. `config/urls.py` mostrando la ruta `noticias/` y el bloque `static(settings.MEDIA_URL, ...)` para desarrollo.
4. `news/models.py` mostrando `Article`, `Category` y `Author`, la imagen destacada, `published_at`, `ForeignKey` y `ManyToManyField`.
5. Terminal con `python manage.py makemigrations news` y `python manage.py migrate` completados.
6. `templates/base.html` mostrando los bloques `title`, `content` y `sidebar`.
7. `news/templates/news/_article_card.html` y una de las plantillas que lo incluyen.
8. Portada en `/noticias/` mostrando las seis noticias, fechas, resúmenes recortados e imágenes.
9. Detalle de una noticia mostrando imagen, autor y categorías.
10. Listado de categoría, por ejemplo `/noticias/categoria/tecnologia/`, mostrando que usa las mismas tarjetas.
11. Administrador con listas de noticias, categorías y autores; en noticias deben verse columnas, filtros y búsqueda.
12. Formulario de una noticia en el administrador con la imagen destacada cargada.
13. Prueba de escapado automático: abre la noticia **Django protege el contenido editorial por defecto**. Debe verse literalmente `<strong>texto HTML de prueba</strong>` y no texto en negrita. Explica que Django escapa HTML por defecto para impedir que el contenido almacenado ejecute etiquetas o scripts.
14. Terminal con `python manage.py check`, `python manage.py makemigrations --check --dry-run` y `python manage.py test` finalizados sin errores.
15. Repositorio de GitHub mostrando los commits y los archivos del portal.

No muestres contraseñas ni datos privados en las capturas.

## Casos de prueba manuales

1. Crear una categoría, un autor y una noticia desde `/admin/`; guardar y comprobar que aparece sin editar código en `/noticias/`.
2. Abrir la noticia y comprobar que el autor, las categorías y la imagen corresponden al registro del administrador.
3. Abrir una categoría y comprobar que solo muestra sus noticias.
4. Buscar una noticia por título y filtrarla por autor o categoría desde el administrador.
5. Cambiar el resumen desde el administrador y recargar la portada; el texto debe cambiar y conservar el recorte de palabras.
6. Guardar una etiqueta HTML en el cuerpo y verificar que se presenta como texto visible, no como marcado ejecutado.
