from datetime import date, timedelta

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from logs.models import log_action
from .models import Loan, Reservation, ReservationStatuses
from .forms import LoanForm, ReservationForm
from django.contrib import messages
from books.models import *
from django.utils import timezone

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loans/loan_list.html', {'loans': loans})

from django.shortcuts import render
from loans.models import Reservation, Loan

def reservation_list(request):
    reservations = Reservation.objects.all()

    active_reservations = []
    issued_reservations = []

    for reservation in reservations:
        loan = Loan.objects.filter(copy=reservation.copy).first()
        if loan:
            issued_reservations.append((reservation, loan.due_date))
        else:
            active_reservations.append(reservation)

    sorted_reservations = active_reservations + issued_reservations

    return render(request, 'loans/reservation_list.html', {
        'sorted_reservations': sorted_reservations,
    })


def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'loans/loan_form.html', {'form': form})

def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'loans/reservation_form.html', {'form': form})


@transaction.atomic
def book_reserve(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copy = BookCopy.objects.filter(book=book, status__status='Доступна').first()

    if not available_copy:
        messages.error(request, 'Нет доступных копий для бронирования.')
        return redirect('book_detail', pk=pk)

    created_status = ReservationStatuses.objects.get(status_name='Создана')
    reservation_end_date = date.today() + timedelta(days=7)

    # Создаём бронирование
    Reservation.objects.create(
        reader=request.user,
        copy=available_copy,
        reservation_end_date=reservation_end_date,
        status=created_status
    )

    # Обновляем статус копии книги
    reserved_status = CopiesStatus.objects.get(status='Забронирована')
    available_copy.status = reserved_status
    available_copy.save()

    messages.success(request, 'Бронирование успешно создано!')
    return redirect('book_detail', pk=pk)


@transaction.atomic
def issue_book(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.status.status_name != 'Создана':
        messages.error(request, 'Невозможно выдать книгу, бронирование не активно.')
        return redirect('reservation_list')

    due_date = timezone.now().date() + timedelta(days=14)
    loan = Loan.objects.create(
        copy=reservation.copy,
        reader=reservation.reader,
        due_date=due_date
    )

    issued_status = CopiesStatus.objects.get(status='Выдана')
    reservation.copy.status = issued_status
    reservation.copy.save()

    messages.success(request, f'Книга успешно выдана. Возврат до {due_date}.')

    return redirect('reservation_list')


@transaction.atomic
def close_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if loan.return_date is not None:
        messages.error(request, 'Эта выдача уже закрыта.')
        return redirect('loan_list')

    loan.return_date = timezone.now()
    loan.save()
    available_status = CopiesStatus.objects.get(status='Доступна')
    loan.copy.status = available_status
    loan.copy.save()

    messages.success(request, 'Выдача успешно закрыта.')
    return redirect('loan_list')
