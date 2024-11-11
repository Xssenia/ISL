from django.urls import path

from . import views
from .views import loan_list, reservation_list, loan_create, reservation_create, close_loan

urlpatterns = [
    path('loans/', loan_list, name='loan_list'),
    path('loans/<int:pk>/close/', close_loan, name='close_loan'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:pk>/issue/', views.issue_book, name='issue_book'),
    path('loans/create/', loan_create, name='loan_create'),
    path('reservations/create/', reservation_create, name='reservation_create'),
    path('books/<int:pk>/reserve/', views.book_reserve, name='book_reserve'),

]
