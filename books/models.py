from django.db import models


class Edition(models.Model):
    edition_name = models.CharField(max_length=255)
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.edition_name


class Author(models.Model):
    author_name = models.CharField(max_length=255)
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=255)
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    deleted_flag = models.BooleanField(default=False)
    authors = models.ManyToManyField(Author, through='BooksAuthors')
    genres = models.ManyToManyField(Genre, through='BooksGenres')

    def __str__(self):
        return self.title


class CopiesStatus(models.Model):
    status = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.status


class BookCopy(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    book_number = models.IntegerField(unique=True)
    status = models.ForeignKey(CopiesStatus, on_delete=models.CASCADE)  # Связь с CopiesStatus
    deleted_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} - Copy {self.book_number} ({self.status})"


class BooksAuthors(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BooksGenres(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
