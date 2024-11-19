from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import User, Role
from django.contrib.auth.decorators import login_required
from loans.models import Reservation, Loan
from users.forms import UserRegistrationForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            reader_role = Role.objects.filter(role_name='Читатель').first()
            if reader_role:
                user.role = reader_role
                user.save()

            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти в систему.')
            return redirect('login')
        else:
            form.add_error(None, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('welcome')
            else:
                form.add_error(None, 'Неверный email или пароль.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRegistrationForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.deleted_flag = True
    user.save()
    return redirect('user_list')


def assign_role(request, user_id, role_id):
    user = get_object_or_404(User, pk=user_id)
    role = get_object_or_404(Role, pk=role_id)
    user.role = role
    user.save()
    return redirect('user_list')


@login_required
def user_reservations_and_loans(request):
    active_reservations = Reservation.objects.filter(
        reader=request.user,
        status__status_name__in=['Создана', 'Активна']
    ).order_by('-reservation_date')

    closed_reservations = Reservation.objects.filter(
        reader=request.user,
        status__status_name__in=['Закрыта', 'Истекла', 'Отменена']
    ).order_by('-reservation_date')

    active_loans = Loan.objects.filter(
        reader=request.user,
        return_date__isnull=True
    ).order_by('-loan_date')

    closed_loans = Loan.objects.filter(
        reader=request.user,
        return_date__isnull=False
    ).order_by('-loan_date')

    context = {
        'active_reservations': active_reservations,
        'closed_reservations': closed_reservations,
        'active_loans': active_loans,
        'closed_loans': closed_loans,
    }
    return render(request, 'users/user_reservations_and_loans.html', context)