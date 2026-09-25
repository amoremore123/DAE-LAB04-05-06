from django.db import models


class Author(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField(unique=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to='authors/', blank=True, null=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'autor'
		verbose_name_plural = 'autores'

	def __str__(self):
		return self.name


class AuthorProfile(models.Model):
	author = models.OneToOneField(
		Author,
		on_delete=models.CASCADE,
		related_name='profile',
	)
	biography = models.TextField()
	website = models.URLField(blank=True)

	class Meta:
		verbose_name = 'perfil de autor'
		verbose_name_plural = 'perfiles de autores'

	def __str__(self):
		return f'Perfil de {self.author}'


class Category(models.Model):
	name = models.CharField(max_length=80, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'categoría'
		verbose_name_plural = 'categorías'

	def __str__(self):
		return self.name


class Publisher(models.Model):
	name = models.CharField(max_length=120, unique=True)
	address = models.CharField(max_length=200, blank=True)
	website = models.URLField(blank=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'editorial'
		verbose_name_plural = 'editoriales'

	def __str__(self):
		return self.name


class Book(models.Model):
	title = models.CharField(max_length=200)
	isbn = models.CharField(max_length=13, unique=True)
	published_date = models.DateField()
	cover = models.ImageField(upload_to='books/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	autor = models.ForeignKey(
		Author,
		on_delete=models.PROTECT,
		related_name='libros',
	)
	categories = models.ManyToManyField(Category, related_name='libros')
	publishers = models.ManyToManyField(
		Publisher,
		through='Publication',
		related_name='libros',
	)

	class Meta:
		ordering = ['title']
		verbose_name = 'libro'
		verbose_name_plural = 'libros'

	def __str__(self):
		return self.title


class BookRating(models.Model):
	book = models.ForeignKey(
		Book,
		on_delete=models.CASCADE,
		related_name='ratings',
	)
	score = models.PositiveSmallIntegerField(
		choices=[(score, f'{score}/5') for score in range(1, 6)],
	)
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'valoración'
		verbose_name_plural = 'valoraciones'

	def __str__(self):
		return f'{self.book}: {self.score}/5'


class Publication(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	publication_date = models.DateField()
	edition = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ['-publication_date']
		constraints = [
			models.UniqueConstraint(
				fields=['book', 'publisher', 'edition'],
				name='unique_book_publisher_edition',
			),
		]
		verbose_name = 'publicación'
		verbose_name_plural = 'publicaciones'

	def __str__(self):
		return f'{self.book} - {self.publisher} (ed. {self.edition})'
