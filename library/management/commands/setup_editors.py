from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from library.models import (
    Author,
    AuthorProfile,
    Book,
    BookRating,
    Category,
    Publication,
    Publisher,
)


class Command(BaseCommand):
    help = 'Crea el grupo editores y un usuario de personal sin permiso para borrar libros.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--email', required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        user_model = get_user_model()
        username = options['username']
        email = options['email']

        if user_model.objects.filter(username=username).exists():
            raise CommandError(f'El usuario {username} ya existe.')

        password = getpass('Contraseña para el usuario editor: ')
        confirmation = getpass('Confirma la contraseña: ')
        if password != confirmation:
            raise CommandError('Las contraseñas no coinciden.')

        candidate_user = user_model(username=username, email=email, is_staff=True)
        try:
            validate_password(password, user=candidate_user)
        except Exception as error:
            raise CommandError(str(error)) from error

        group, _ = Group.objects.get_or_create(name='editores')
        model_permissions = {
            Book: ('view', 'add', 'change'),
            BookRating: ('view', 'add', 'change'),
            Publication: ('view', 'add', 'change'),
            Author: ('view',),
            AuthorProfile: ('view',),
            Category: ('view',),
            Publisher: ('view',),
        }
        permissions = []
        for model, actions in model_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            codenames = [f'{action}_{model._meta.model_name}' for action in actions]
            permissions.extend(
                Permission.objects.filter(
                    content_type=content_type,
                    codename__in=codenames,
                )
            )
        group.permissions.set(permissions)

        user = user_model.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=False,
        )
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f'Usuario {username} agregado al grupo editores. '
            'No tiene permiso para eliminar libros.'
        ))
