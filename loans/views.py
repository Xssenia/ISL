from django.shortcuts import render, redirect, get_object_or_404
from .models import Loan, Reservation
from .forms import LoanForm, ReservationForm

def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loans/loan_list.html', {'loans': loans})

def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'loans/reservation_list.html', {'reservations': reservations})

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

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from books.models import *
from django.utils import timezone

def book_reserve(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Находим копию книги со статусом "Доступна"
    available_copy = BookCopy.objects.filter(book=book, status=1).first()

    if available_copy:
        # Обновляем статус копии книги на "Забронирована"
        available_copy.status = 3  # "Забронирована"
        available_copy.save()

        # Создаем запись в таблице бронирований
        reservation_status = ReservationStatuses.objects.get(status_name='Создана')
        reservation = Reservation.objects.create(
            reader_id=request.user.id,
            copy_id=available_copy.pk,
            status_id=reservation_status.pk,
            reservation_date=timezone.now(),
            reservation_end_date=timezone.now() + timezone.timedelta(days=7)
        )

        messages.success(request, "Бронирование успешно создано.")
        return redirect('catalog')
    else:
        messages.error(request, "Нет доступных копий для бронирования.")
        return redirect('book_detail', pk=pk)
