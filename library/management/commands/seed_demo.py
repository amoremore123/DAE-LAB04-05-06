from datetime import date

from django.core.management.base import BaseCommand

from library.models import Author, AuthorProfile, Book, Category, Publication, Publisher


class Command(BaseCommand):
    help = 'Carga los datos de demostracion del laboratorio.'

    def handle(self, *args, **options):
        authors = [
            {
                'name': 'Gabriel Garcia Marquez',
                'email': 'gabriel@example.com',
                'birth_date': date(1927, 3, 6),
                'biography': 'Autor colombiano y referente del realismo magico.',
            },
            {
                'name': 'Isabel Allende',
                'email': 'isabel@example.com',
                'birth_date': date(1942, 8, 2),
                'biography': 'Escritora chilena de narrativa y memoria.',
            },
        ]
        author_objects = []
        for data in authors:
            author, _ = Author.objects.update_or_create(
                email=data['email'],
                defaults={
                    'name': data['name'],
                    'birth_date': data['birth_date'],
                },
            )
            AuthorProfile.objects.update_or_create(
                author=author,
                defaults={'biography': data['biography'], 'website': 'https://example.com'},
            )
            author_objects.append(author)

        category_names = ['Novela', 'Realismo magico', 'Literatura latinoamericana']
        categories = {
            name: Category.objects.get_or_create(name=name)[0]
            for name in category_names
        }

        publisher_data = [
            ('Editorial Sudamericana', 'Buenos Aires'),
            ('Plaza & Janes', 'Barcelona'),
        ]
        publishers = {
            name: Publisher.objects.get_or_create(name=name, defaults={'address': address})[0]
            for name, address in publisher_data
        }

        books = [
            ('Cien años de soledad', '9780307474728', date(1967, 5, 30), author_objects[0], ['Novela', 'Realismo magico'], 'Editorial Sudamericana', 1),
            ('El amor en los tiempos del colera', '9780307389732', date(1985, 9, 5), author_objects[0], ['Novela'], 'Editorial Sudamericana', 2),
            ('La casa de los espiritus', '9781501117015', date(1982, 1, 1), author_objects[1], ['Novela', 'Realismo magico', 'Literatura latinoamericana'], 'Plaza & Janes', 1),
            ('Paula', '9780061564902', date(1994, 1, 1), author_objects[1], ['Literatura latinoamericana'], 'Plaza & Janes', 3),
        ]
        for title, isbn, published_date, author, category_list, publisher_name, edition in books:
            book, _ = Book.objects.update_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'published_date': published_date,
                    'autor': author,
                },
            )
            book.categories.set([categories[name] for name in category_list])
            Publication.objects.update_or_create(
                book=book,
                publisher=publishers[publisher_name],
                edition=edition,
                defaults={'publication_date': published_date},
            )

        self.stdout.write(self.style.SUCCESS(
            'Datos cargados: 2 autores, 4 libros, 3 categorias y 2 editoriales.'
        ))
