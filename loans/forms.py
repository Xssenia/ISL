from django import forms
from .models import Loan, Reservation


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['reader', 'copy', 'due_date']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reader', 'copy', 'reservation_end_date', 'status']
