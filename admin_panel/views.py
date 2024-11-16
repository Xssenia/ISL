from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm
from users.models import User
from .models import Log
from users.views import User


def log_action(user, action_type, entity, entity_id, details=None):
    Log.objects.create(
        user=user,
        type=action_type,
        entity=entity,
        entityID=entity_id,
        action_details=details
    )

@login_required
def admin_view_logs(request):
    if not request.user.is_authenticated or request.user.role is None or request.user.role.role_name != 'Администратор':
        return redirect('welcome')

    logs = Log.objects.select_related('user').order_by('-time')
    users = User.objects.filter(is_active=True)

    action_type = request.GET.get('type')
    user_id = request.GET.get('user_id')

    if action_type:
        logs = logs.filter(type=action_type)
    if user_id:
        logs = logs.filter(user_id=user_id)

    return render(request, 'admin_db/logs.html', {
        'logs': logs,
        'users': users,
        'action_type': action_type,
        'user_id': user_id,
    })


@login_required
def admin_user_list(request):
    if not request.user.is_authenticated or request.user.role is None or request.user.role.role_name != 'Администратор':
        return redirect('welcome')
    users = User.objects.filter(deleted_flag=False)
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
def admin_add_user(request):
    if not request.user.is_authenticated or request.user.role is None or request.user.role.role_name != 'Администратор':
        return redirect('welcome')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin_user_list')
    else:
        form = UserForm()
    return render(request, 'admin/add_user.html', {'form': form})

@login_required
def admin_edit_user(request, pk):
    if not request.user.is_authenticated or request.user.role is None or request.user.role.role_name != 'Администратор':
        return redirect('welcome')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

@login_required
def admin_delete_user(request, pk):
    if not request.user.is_authenticated or request.user.role is None or request.user.role.role_name != 'Администратор':
        return redirect('welcome')
    user = get_object_or_404(User, pk=pk)
    user.deleted_flag = True
    user.save()
    return redirect('admin_user_list')
