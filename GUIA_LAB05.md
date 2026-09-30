# Laboratorio 05 - Administrador de Django para la biblioteca

## Adaptación del caso

Se conserva el dominio de biblioteca de los laboratorios anteriores. Los conceptos del enunciado de películas se adaptan así:

| Enunciado original | Proyecto acumulativo |
|---|---|
| `Movie` | `Book` |
| `Genre` | `Category` |
| `Person` | `Author` |
| `Rating` | `BookRating` |

`Publisher`, `Publication` y `AuthorProfile` siguen formando parte del catálogo y también se administran.

## 1. Preparar el entorno

Desde PowerShell, en la carpeta `DAE-Lab04-05-06`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

El catálogo público está en `http://127.0.0.1:8000/` y el administrador en `http://127.0.0.1:8000/admin/`.

`seed_demo` deja diez libros, cuatro categorías, dos autores, dos editoriales y cinco valoraciones de ejemplo. El comando es idempotente: se puede ejecutar otra vez sin duplicar los registros. Para la evidencia, se deben mostrar estos datos desde el administrador y se pueden editar allí.

## 2. Modelos y registro en el administrador

Los modelos gestionados son `Author`, `AuthorProfile`, `Book`, `BookRating`, `Category`, `Publisher` y `Publication`. `BookRating` guarda una puntuación de 1 a 5 y un comentario; cada valoración pertenece a un libro.

En `library/admin.py` se utilizan clases `ModelAdmin`. El listado de libros muestra título, autor, ISBN, fecha y creación; ofrece filtros por categoría, fecha y autor, y búsqueda por título, ISBN y nombre de autor.

Las publicaciones y valoraciones se editan en líneas dentro del formulario del libro. El perfil biográfico se edita en línea dentro del formulario del autor. Los campos de auditoría `created_at` y `updated_at` son de solo lectura en el admin.

## 3. Crear el usuario editor

Después de aplicar migraciones, se configura el grupo y el usuario desde PowerShell:

```powershell
python manage.py setup_editors --username editor --email editor@example.com
```

El comando solicita la contraseña dos veces y no la muestra ni la guarda en el código. El usuario pertenece al grupo `editores`, tiene acceso al admin y puede ver, añadir y cambiar libros, valoraciones y publicaciones. Puede consultar los demás catálogos, pero no tiene permiso para borrar libros. No es superusuario.

Para comprobarlo, inicia sesión en `/admin/` como superusuario y abre **Autenticación y autorización → Grupos → editores** para mostrar los permisos. Después cierra esa sesión, entra como `editor` y abre **Libros**. Deben estar disponibles las acciones permitidas; el usuario no debe ver la acción de eliminación. No incluyas contraseñas en capturas.

## 4. Recomendaciones públicas

La vista `book_recommendations` muestra libros que comparten al menos una categoría con el libro seleccionado y que tienen valoraciones. Ordena por promedio de puntuación, luego por número de valoraciones y finalmente por título. No presenta el libro de partida ni libros de categorías distintas.

Desde cualquier ficha se accede a **Explorar libros relacionados**. Por ejemplo:

```text
http://127.0.0.1:8000/libros/1/recomendaciones/
```

Esto permite contrastar el administrador, que gestiona registros, con una vista pública propia que consulta y presenta datos relacionados.

## 5. Pruebas

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Las pruebas comprueban las relaciones, el borrado protegido, el usuario editor sin permiso de eliminación y las recomendaciones por categoría y promedio de puntuación.

## 6. Capturas para el entregable

1. Estructura del proyecto en VS Code mostrando `config`, `library`, `manage.py` y las migraciones.
2. Panel del superusuario antes de personalizar o, si se entrega el estado final, listado de libros personalizado.
3. `library/admin.py` mostrando `list_display`, `list_filter` y `search_fields` de libros.
4. Formulario de libro mostrando publicaciones y valoraciones como líneas.
5. Formulario de autor mostrando el perfil en línea.
6. Campos `created_at` y `updated_at` marcados como solo lectura en el formulario del libro.
7. Listados del admin con diez libros, cuatro categorías y cinco valoraciones como mínimo.
8. Grupo `editores` mostrando permisos para ver, añadir y cambiar libros, sin `delete_book`.
9. Panel del superusuario y panel del editor, sin credenciales visibles.
10. Vista pública de recomendaciones mostrando coincidencia de categorías y puntuación.
11. Salida de `python manage.py test` con todas las pruebas en `OK`.

## Observaciones

- Se mantiene el modelo de biblioteca acumulativo y se sustituyen los nombres del dominio de películas por conceptos equivalentes del catálogo.
- `BookRating` es el equivalente didáctico de la valoración original.
- El editor tiene permisos limitados por grupo; el superusuario conserva acceso completo.
- El servidor incluido por `runserver` es únicamente para desarrollo.