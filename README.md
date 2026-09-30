# DAE Labs 04, 05 y 06

Proyecto acumulativo de Desarrollo de Aplicaciones Empresariales sobre una biblioteca digital. Se conserva el dominio de autores, libros, categorías y editoriales para desarrollar los laboratorios 04, 05 y 06 en una sola aplicación Django.

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
python manage.py createsuperuser
python manage.py runserver
```

- Catálogo: http://127.0.0.1:8000/
- Administración: http://127.0.0.1:8000/admin/

La base SQLite y el entorno virtual son locales y no se versionan. Las migraciones sí se guardan en Git.

## Estado de los laboratorios

- Lab 04: modelos y relaciones de la biblioteca, consultas y vista pública.
- Lab 05: administración personalizada, valoraciones, permisos y recomendaciones.
- Lab 06: se incorporará al mismo proyecto cuando se defina el procedimiento de la sesión.
