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
