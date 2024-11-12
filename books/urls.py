from django.urls import path

from . import views
from .views import book_list, book_detail, book_create, book_update, book_delete, author_delete

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('catalog/', views.book_list_reader, name='book_list_reader'),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('create/', book_create, name='book_create'),
    path('<int:pk>/update/', book_update, name='book_update'),
    path('<int:pk>/delete/', book_delete, name='book_delete'),
    path('deleted_books/', views.deleted_books, name='deleted_books'),
    path('restore_book/<int:pk>/', views.restore_book, name='restore_book'),
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/add/', views.GenreCreateView.as_view(), name='genre_add'),
    path('genres/<int:pk>/edit/', views.GenreUpdateView.as_view(), name='genre_edit'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),
    path('deleted_genres/', views.deleted_genres, name='deleted_genres'),
    path('restore_genre/<int:pk>/', views.restore_genre, name='restore_genre'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<int:pk>/delete/', author_delete, name='author_delete'),
    path('deleted_authors/', views.deleted_authors, name='deleted_authors'),
    path('restore_author/<int:pk>/', views.restore_author, name='restore_author'),
    path('editions/', views.EditionListView.as_view(), name='edition_list'),
    path('editions/add/', views.EditionCreateView.as_view(), name='edition_add'),
    path('editions/<int:pk>/edit/', views.EditionUpdateView.as_view(), name='edition_edit'),
    path('editions/<int:pk>/delete/', views.EditionDeleteView.as_view(), name='edition_delete'),
    path('deleted_editions/', views.DeletedEditionListView.as_view(), name='deleted_editions'),
    path('restore_edition/<int:pk>/', views.restore_edition, name='restore_edition'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('copies/', views.book_copy_list, name='book_copy_list'),
    path('copies/create/', views.book_copy_create, name='book_copy_create'),
    path('copies/<int:pk>/edit/', views.book_copy_edit, name='book_copy_edit'),
    path('copies/<int:pk>/delete/', views.book_copy_delete, name='book_copy_delete'),
    path('deleted_bookcopies/', views.DeletedBookCopyListView.as_view(), name='deleted_bookcopies'),
    path('restore_bookcopy/<int:pk>/', views.book_copy_restore, name='book_copy_restore'),
]

