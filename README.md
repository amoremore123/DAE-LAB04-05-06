# DAE Labs 04, 05 y 06

Proyecto acumulativo de Desarrollo de Aplicaciones Empresariales. Conserva la biblioteca digital de los laboratorios 04 y 05, e incorpora el portal de noticias del laboratorio 06 como una aplicación independiente.

## Requisitos

- Python 3.12 o superior
- Git
- Windows / PowerShell

## Configuración local

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py seed_news_demo
python manage.py createsuperuser
python manage.py runserver
```

- Catálogo: http://127.0.0.1:8000/
- Noticias: http://127.0.0.1:8000/noticias/
- Administración: http://127.0.0.1:8000/admin/

La base SQLite y el entorno virtual son locales y no se versionan. Las migraciones sí se guardan en Git.

## Estado de los laboratorios

- Lab 04: modelos y relaciones de la biblioteca, consultas y vista pública.
- Lab 05: administración personalizada, valoraciones, permisos y recomendaciones.
- Lab 06: portal de noticias con plantillas heredadas, fragmentos reutilizables, archivos estáticos y medios.
