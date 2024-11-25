from django import forms
from .models import *

from django import forms

from django import forms
from .models import Book, Author, Genre, Edition

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label='Авторы'
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label='Жанры'
    )
    edition = forms.ModelChoiceField(
        queryset=Edition.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=True,
        label='Издание'
    )

    publication_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите год публикации'
        }),
        label='Год публикации'
    )

    cover_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        }),
        label='Обложка книги'
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите описание книги'
        }),
        label='Описание'
    )

    class Meta:
        model = Book
        fields = ['title', 'edition', 'authors', 'genres', 'publication_year', 'cover_image', 'description']
        labels = {
            'title': 'Название книги',
            'edition': 'Издание',
            'publication_year': 'Год публикации',
            'cover_image': 'Обложка книги',
            'description': 'Описание',
        }



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author_name']
        labels = {
            'author_name': 'Имя автора',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']
        labels = {
            'genre_name': 'Название жанра',
        }

class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['edition_name']
        labels = {
            'edition_name': 'Название издательства',
        }

class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'book_number', 'status']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'book_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'book': 'Название книги',
            'book_number': 'Номер копии',
            'status': 'Статус'
        }

