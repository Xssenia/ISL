from django import forms
from .models import *

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Авторы'
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Жанры'
    )
    edition = forms.ModelChoiceField(
        queryset=Edition.objects.all(),
        required=True,
        label='Издание'
    )

    class Meta:
        model = Book
        fields = ['title', 'edition', 'authors', 'genres', 'publication_year', 'cover_image', 'description']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['author_name']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']

class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'book_number', 'status']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'book_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

