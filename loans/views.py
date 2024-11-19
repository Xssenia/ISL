from datetime import date, timedelta
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Loan, Reservation, ReservationStatuses
from .forms import LoanForm, ReservationForm
from django.contrib import messages
from books.models import *
from django.utils import timezone


def loan_list(request):
    loans = Loan.objects.all()

    active_loans = loans.filter(return_date__isnull=True).order_by('-loan_date')
    closed_loans = loans.filter(return_date__isnull=False).order_by('-return_date')

    return render(request, 'loans/loan_list.html', {
        'active_loans': active_loans,
        'closed_loans': closed_loans,
    })


def reservation_list(request):
    active_reservations = Reservation.objects.filter(
        status__status_name__in=['Создана', 'Активна']
    ).order_by('-reservation_date')

    issued_reservations = Reservation.objects.filter(
        status__status_name='Закрыта'
    ).order_by('-reservation_date')

    sorted_reservations = list(active_reservations) + list(issued_reservations)

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


@transaction.atomic
def book_reserve(request, pk):
    book = get_object_or_404(Book, pk=pk)
    available_copy = BookCopy.objects.filter(book=book, status__status='Доступна').first()

    if not available_copy:
        messages.error(request, 'Нет доступных копий для бронирования.')
        return redirect('book_detail', pk=pk)

    created_status = ReservationStatuses.objects.get(status_name='Создана')
    reservation_end_date = date.today() + timedelta(days=7)

    Reservation.objects.create(
        reader=request.user,
        copy=available_copy,
        reservation_end_date=reservation_end_date,
        status=created_status
    )

    reserved_status = CopiesStatus.objects.get(status='Забронирована')
    available_copy.status = reserved_status
    available_copy.save()

    messages.success(request, 'Бронирование успешно создано!')
    return redirect('book_detail', pk=pk)


@transaction.atomic
def issue_book(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.status.status_name not in ['Создана', 'Активна']:
        messages.error(request, 'Эту бронь нельзя выдать, так как она уже закрыта или истекла.')
        return redirect('reservation_list')

    due_date = timezone.now().date() + timedelta(days=14)
    Loan.objects.create(
        reader=reservation.reader,
        copy=reservation.copy,
        loan_date=timezone.now().date(),
        due_date=due_date,
    )

    closed_status = ReservationStatuses.objects.get(status_name='Закрыта')
    reservation.status = closed_status
    reservation.save()

    issued_status = CopiesStatus.objects.get(status='Выдана')
    reservation.copy.status = issued_status
    reservation.copy.save()

    messages.success(request, 'Книга успешно выдана, бронирование закрыто.')
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