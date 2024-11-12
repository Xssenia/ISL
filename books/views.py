from datetime import date

from django.shortcuts import render, redirect, get_object_or_404

from loans.models import Reservation
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from logs.models import log_action

def book_list(request):
    genre_filter = request.GET.get('genre')
    author_filter = request.GET.get('author')
    title_filter = request.GET.get('title')

    books = Book.objects.filter(deleted_flag=False)

    if genre_filter:
        books = books.filter(genre__genre_name__icontains=genre_filter)
    if author_filter:
        books = books.filter(author__author_name__icontains=author_filter)
    if title_filter:
        books = books.filter(title__icontains=title_filter)

    genres = Genre.objects.filter(deleted_flag=False)
    authors = Author.objects.filter(deleted_flag=False)

    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genres,
        'authors': authors,
        'selected_genre': genre_filter,
        'selected_author': author_filter,
        'selected_title': title_filter
    })

def book_detail(request, pk):
    book = get_object_or_404(Book.objects.prefetch_related('authors', 'genres'), pk=pk)

    user_has_active_reservation = False
    is_librarian = False

    if request.user.is_authenticated:
        # Проверяем, является ли пользователь библиотекарем
        is_librarian = request.user.role.role_name == 'Библиотекарь'

        # Проверка активных бронирований
        active_reservation_exists = Reservation.objects.filter(
            reader=request.user,
            copy__book=book,
            status__status_name__in=['Создана', 'Активна'],
            reservation_end_date__gte=date.today()
        ).exists()

        if active_reservation_exists:
            user_has_active_reservation = True

        # Проверка завершённых бронирований
        closed_reservation_exists = Reservation.objects.filter(
            reader=request.user,
            copy__book=book,
            status__status_name__in=['Закрыта', 'Истекла', 'Отменена']
        ).exists()

        if not active_reservation_exists and closed_reservation_exists:
            user_has_active_reservation = False

    return render(
        request,
        template_name='books/book_detail.html',
        context={
            'book': book,
            'user_has_active_reservation': user_has_active_reservation,
            'is_librarian': is_librarian,
        }
    )




def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()

            authors = form.cleaned_data['authors']
            for author in authors:
                BooksAuthors.objects.get_or_create(book=book, author=author)

            genres = form.cleaned_data['genres']
            for genre in genres:
                BooksGenres.objects.get_or_create(book=book, genre=genre)

            log_action(request.user, 'CREATE', 'Book', book.id, f"Создана книга {book.title}")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.deleted_flag = True
    book.save()
    return redirect('book_list')

class GenreListView(ListView):
    model = Genre
    template_name = 'genres/genre_list.html'
    context_object_name = 'genres'

    def get_queryset(self):
        return Genre.objects.filter(deleted_flag=False)

class GenreCreateView(CreateView):
    model = Genre
    fields = ['genre_name']
    template_name = 'genres/genre_form.html'
    success_url = reverse_lazy('genre_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request.user, 'CREATE', 'Genre', self.object.id, f"Создан жанр {self.object.genre_name}")
        return response

class GenreUpdateView(UpdateView):
    model = Genre
    fields = ['genre_name']
    template_name = 'genres/genre_form.html'
    success_url = reverse_lazy('genre_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request.user, 'UPDATE', 'Genre', self.object.id, f"Обновлен жанр {self.object.genre_name}")
        return response

class AuthorListView(ListView):
    model = Author
    template_name = 'authors/author_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return Author.objects.filter(deleted_flag=False)

class AuthorCreateView(CreateView):
    model = Author
    fields = ['author_name']
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('author_list')

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['author_name']
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('author_list')

class EditionListView(ListView):
    model = Edition
    template_name = 'editions/edition_list.html'
    context_object_name = 'editions'

    def get_queryset(self):
        return Edition.objects.filter(deleted_flag=False)


class EditionCreateView(CreateView):
    model = Edition
    fields = ['edition_name']
    template_name = 'editions/edition_form.html'
    success_url = reverse_lazy('edition_list')

class EditionUpdateView(UpdateView):
    model = Edition
    fields = ['edition_name']
    template_name = 'editions/edition_form.html'
    success_url = reverse_lazy('edition_list')

class GenreDeleteView(View):
    def get(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        genre.deleted_flag = True
        genre.save()
        return redirect(reverse_lazy('genre_list'))

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.deleted_flag = True
    author.save()
    log_action(request.user, 'DELETE', 'Author', author.id, f"Автор {author.author_name} был удален")
    return redirect(reverse_lazy('author_list'))


class EditionDeleteView(View):
    def get(self, request, pk):
        edition = get_object_or_404(Edition, pk=pk)
        edition.deleted_flag = True
        edition.save()
        log_action(request.user, 'DELETE', 'Edition', edition.id, f"Издание {edition.edition_name} было удалено")
        return redirect(reverse_lazy('edition_list'))

class DeletedEditionListView(ListView):
    model = Edition
    template_name = 'editions/deleted_editions.html'
    context_object_name = 'deleted_editions'

    def get_queryset(self):
        return Edition.objects.filter(deleted_flag=True)

def book_list_reader(request):
    query = request.GET.get('q', '')
    author_filter = request.GET.get('author', '')
    genre_filter = request.GET.get('genre', '')

    books = Book.objects.filter(deleted_flag=False)

    if query:
        books = books.filter(title__icontains=query)
    if author_filter:
        books = books.filter(authors__author_name__icontains=author_filter)
    if genre_filter:
        books = books.filter(genres__genre_name__icontains=genre_filter)

    books = books.distinct()

    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    authors = Author.objects.filter(deleted_flag=False)
    genres = Genre.objects.filter(deleted_flag=False)

    return render(request, 'books/book_list_reader.html', {
        'page_obj': page_obj,
        'query': query,
        'author_filter': author_filter,
        'genre_filter': genre_filter,
        'authors': authors,
        'genres': genres,
    })

def book_copy_list(request):
    copies = BookCopy.objects.filter(deleted_flag=False)
    return render(request, 'book_copies/book_copy_list.html', {'copies': copies})

class BookCopyListView(ListView):
    model = BookCopy
    template_name = 'book_copies/book_copy_list.html'
    context_object_name = 'book_copies'

    def get_queryset(self):
        return BookCopy.objects.filter(deleted_flag=False)

def book_copy_create(request):
    if request.method == 'POST':
        form = BookCopyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_copy_list')
    else:
        form = BookCopyForm()
    return render(request, 'book_copies/book_copy_form.html', {'form': form})

def book_copy_edit(request, pk):
    copy = get_object_or_404(BookCopy, pk=pk)
    if request.method == 'POST':
        form = BookCopyForm(request.POST, instance=copy)
        if form.is_valid():
            form.save()
            return redirect('book_copy_list')
    else:
        form = BookCopyForm(instance=copy)
    return render(request, 'book_copies/book_copy_form.html', {'form': form})

def book_copy_delete(request, pk):
    book_copy = get_object_or_404(BookCopy, pk=pk)
    book_copy.deleted_flag = True
    book_copy.save()
    log_action(request.user, 'DELETE', 'BookCopy', book_copy.id, f"Копия книги {book_copy.book.title} была удалена")
    return redirect('book_copy_list')

class DeletedBookCopyListView(ListView):
    model = BookCopy
    template_name = 'book_copies/deleted_book_copies.html'
    context_object_name = 'deleted_book_copies'

    def get_queryset(self):
        return BookCopy.objects.filter(deleted_flag=True)

def book_copy_restore(request, pk):
    book_copy = get_object_or_404(BookCopy, pk=pk, deleted_flag=True)
    book_copy.deleted_flag = False
    book_copy.save()
    log_action(request.user, 'RESTORE', 'BookCopy', book_copy.id, f"Копия книги {book_copy.book.title} была восстановлена")
    return redirect('book_copy_list')

def deleted_books(request):
    books = Book.objects.filter(deleted_flag=True)
    return render(request, 'books/deleted_books.html', {'books': books})

def restore_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.deleted_flag = False
    book.save()
    return redirect('book_list')

def deleted_authors(request):
    authors = Author.objects.filter(deleted_flag=True)
    return render(request, 'authors/deleted_authors.html', {'authors': authors})

def restore_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.deleted_flag = False
    author.save()
    return redirect('author_list')

def deleted_genres(request):
    genres = Genre.objects.filter(deleted_flag=True)
    return render(request, 'genres/deleted_genres.html', {'genres': genres})

def restore_genre(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    genre.deleted_flag = False
    genre.save()
    log_action(request.user, 'RESTORE', 'Genre', genre.id, f"Жанр {genre.genre_name} был восстановлен")
    return redirect('genre_list')

def restore_edition(request, pk):
    edition = get_object_or_404(Edition, pk=pk, deleted_flag=True)
    edition.deleted_flag = False
    edition.save()
    log_action(request.user, 'RESTORE', 'Edition', edition.id, f"Издание {edition.edition_name} было восстановлено")
    return redirect('edition_list')


def welcome(request):
    return render(request, 'users/welcome.html')