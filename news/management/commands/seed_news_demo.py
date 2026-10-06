from datetime import datetime
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Article, Author, Category


class Command(BaseCommand):
    help = 'Carga seis noticias de demostracion para el portal.'

    def handle(self, *args, **options):
        author_data = [
            {
                'name': 'Mariana Reyes',
                'email': 'mariana.reyes@example.com',
                'biography': 'Periodista interesada en cultura digital y comunidades locales.',
            },
            {
                'name': 'Diego Salas',
                'email': 'diego.salas@example.com',
                'biography': 'Redactor de ciencia y tecnologia aplicada.',
            },
            {
                'name': 'Lucia Paredes',
                'email': 'lucia.paredes@example.com',
                'biography': 'Cronista de iniciativas ciudadanas y proyectos culturales.',
            },
        ]
        authors = {}
        for data in author_data:
            author, _ = Author.objects.update_or_create(
                email=data['email'],
                defaults={
                    'name': data['name'],
                    'biography': data['biography'],
                },
            )
            authors[data['email']] = author

        category_data = [
            {
                'name': 'Tecnología',
                'slug': 'tecnologia',
                'description': 'Herramientas digitales, software y aprendizaje tecnico.',
            },
            {
                'name': 'Cultura',
                'slug': 'cultura',
                'description': 'Historias, actividades y expresiones culturales de la comunidad.',
            },
            {
                'name': 'Comunidad',
                'slug': 'comunidad',
                'description': 'Personas, proyectos y espacios que conectan el entorno local.',
            },
        ]
        categories = {}
        for data in category_data:
            category, _ = Category.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                },
            )
            categories[data['slug']] = category

        article_data = [
            {
                'title': 'El aula abre un espacio para proyectos con Django',
                'slug': 'el-aula-abre-un-espacio-para-proyectos-con-django',
                'summary': 'Estudiantes presentan portales web que conectan datos, plantillas y contenido administrable.',
                'body': 'El nuevo espacio de trabajo permite publicar proyectos web con una estructura ordenada.\n\nCada equipo puede administrar noticias desde Django y ver los cambios de inmediato en el portal.',
                'author': 'mariana.reyes@example.com',
                'categories': ['tecnologia', 'comunidad'],
                'published_at': datetime(2026, 10, 6, 9, 0),
                'color': '#334e68',
            },
            {
                'title': 'Una biblioteca de barrio recupera historias en voz alta',
                'slug': 'una-biblioteca-de-barrio-recupera-historias-en-voz-alta',
                'summary': 'Lectores y vecinos se reunen cada viernes para compartir relatos que circulan fuera de las pantallas.',
                'body': 'La actividad convierte la lectura en una conversacion entre generaciones.\n\nLos organizadores preparan una seleccion mensual de autores locales.',
                'author': 'lucia.paredes@example.com',
                'categories': ['cultura', 'comunidad'],
                'published_at': datetime(2026, 10, 5, 15, 30),
                'color': '#7b5e57',
            },
            {
                'title': 'Pequenos laboratorios prueban ideas para una ciudad mas amable',
                'slug': 'pequenos-laboratorios-prueban-ideas-para-una-ciudad-mas-amable',
                'summary': 'Un grupo interdisciplinario transforma problemas cotidianos en prototipos abiertos a la comunidad.',
                'body': 'Las propuestas nacen de observar recorridos, tiempos de espera y espacios compartidos.\n\nEl siguiente encuentro mostrara los primeros resultados a vecinos y estudiantes.',
                'author': 'diego.salas@example.com',
                'categories': ['tecnologia', 'comunidad'],
                'published_at': datetime(2026, 10, 4, 11, 15),
                'color': '#526f52',
            },
            {
                'title': 'El archivo fotografico suma nuevas memorias familiares',
                'slug': 'el-archivo-fotografico-suma-nuevas-memorias-familiares',
                'summary': 'Una convocatoria publica recibe imagenes y testimonios para ampliar la historia visual del distrito.',
                'body': 'Cada fotografia se registra con una fecha aproximada y la historia de quien la conserva.\n\nEl archivo estara disponible para consulta en formato digital y presencial.',
                'author': 'lucia.paredes@example.com',
                'categories': ['cultura'],
                'published_at': datetime(2026, 10, 3, 10, 45),
                'color': '#9a6b3f',
            },
            {
                'title': 'Django protege el contenido editorial por defecto',
                'slug': 'django-protege-el-contenido-editorial-por-defecto',
                'summary': 'El escapado automatico evita que el texto de una noticia se interprete como codigo HTML en la pagina.',
                'body': 'Esta noticia guarda la etiqueta <strong>texto HTML de prueba</strong> como contenido. La plantilla la muestra como texto para proteger el portal.',
                'author': 'diego.salas@example.com',
                'categories': ['tecnologia'],
                'published_at': datetime(2026, 10, 2, 14, 0),
                'color': '#734a5e',
            },
            {
                'title': 'Una feria creativa convierte la plaza en taller abierto',
                'slug': 'una-feria-creativa-convierte-la-plaza-en-taller-abierto',
                'summary': 'Musica, ilustracion y oficios locales compartiran una jornada para todas las edades.',
                'body': 'La feria reunira demostraciones, conversaciones breves y puestos de creadores independientes.\n\nLa entrada sera libre durante toda la jornada.',
                'author': 'mariana.reyes@example.com',
                'categories': ['cultura', 'comunidad'],
                'published_at': datetime(2026, 10, 1, 16, 20),
                'color': '#3e6473',
            },
        ]

        for data in article_data:
            article, _ = Article.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'summary': data['summary'],
                    'body': data['body'],
                    'author': authors[data['author']],
                    'published_at': timezone.make_aware(data['published_at']),
                },
            )
            article.categories.set([categories[slug] for slug in data['categories']])
            if not article.featured_image:
                article.featured_image.save(
                    f"{article.slug}.jpg",
                    self.create_image(data['color']),
                    save=True,
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Datos cargados: 3 autores, 3 categorias y 6 noticias con imagenes.'
            )
        )

    @staticmethod
    def create_image(color):
        image = Image.new('RGB', (1200, 675), color)
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        return ContentFile(buffer.getvalue())
