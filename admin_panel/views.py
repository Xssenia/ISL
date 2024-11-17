from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.utils import timezone
from django.conf import settings
import os

from .forms import UserEditForm, AdminUserCreationForm
from .models import Log
from users.models import User, Role

BACKUP_DIR = os.path.join("admin_panel", "backups")

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
    if not request.user.role or request.user.role.role_name != 'Администратор':
        return redirect('welcome')

    logs = Log.objects.select_related('user').order_by('-time')
    users = User.objects.filter(is_active=True)

    action_type = request.GET.get('type')
    user_id = request.GET.get('user_id')

    if action_type:
        logs = logs.filter(type=action_type)
    if user_id:
        logs = logs.filter(user_id=user_id)

    log_action(request.user, 'VIEW', 'Logs', 0, 'Просмотр логов')
    return render(request, 'admin_db/logs.html', {
        'logs': logs,
        'users': users,
        'action_type': action_type,
        'user_id': user_id,
    })

@login_required
def backup_db(request):
    if not request.user.role or request.user.role.role_name != 'Администратор':
        messages.error(request, 'У вас нет прав для выполнения этой операции.')
        return render(request, 'admin_db/backup_restore.html')

    if request.method == 'POST':
        try:
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)

            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")

            os.system(f"python manage.py dumpdata > {backup_file}")
            log_action(request.user, 'SAVE_DB', 'Database', 0, f"База данных сохранена в файл: {backup_file}")
            messages.success(request, f'База данных успешно сохранена в файл: {backup_file}')
        except Exception as e:
            messages.error(request, f'Ошибка при сохранении базы данных: {str(e)}')

    return render(request, 'admin_db/backup_restore.html')

@login_required
def restore_db(request):
    if not request.user.role or request.user.role.role_name != 'Администратор':
        messages.error(request, 'У вас нет прав для выполнения этой операции.')
        return render(request, 'admin_db/backup_restore.html')

    if request.method == 'POST':
        backup_file = request.FILES.get('backup_file')
        if not backup_file:
            messages.error(request, 'Файл резервной копии не был загружен.')
            return render(request, 'admin_db/backup_restore.html')

        try:
            backup_path = default_storage.save(f"admin_panel/backups/{backup_file.name}", backup_file)
            os.system(f"python manage.py loaddata {backup_path}")
            log_action(request.user, 'RESTORE_DB', 'Database', 0, f"База данных восстановлена из файла: {backup_file.name}")
            messages.success(request, f'База данных успешно восстановлена из файла: {backup_file.name}.')
        except Exception as e:
            messages.error(request, f'Ошибка при восстановлении базы данных: {str(e)}')

    return render(request, 'admin_db/backup_restore.html')

@login_required
def admin_user_list(request):
    if not request.user.role or request.user.role.role_name != 'Администратор':
        messages.error(request, 'У вас нет прав для просмотра этой страницы.')
        return redirect('welcome')

    users = User.objects.select_related('role').order_by('-is_active', 'email')
    role_filter = request.GET.get('role')
    if role_filter and role_filter != 'Все':
        users = users.filter(role__role_name=role_filter)

    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(email__icontains=search_query)

    roles = Role.objects.all()
    log_action(request.user, 'VIEW', 'UserList', 0, 'Просмотр списка пользователей')
    return render(request, 'admin_db/user_list.html', {
        'users': users,
        'roles': roles,
        'role_filter': role_filter,
        'search_query': search_query,
    })

@login_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    log_action(request.user, 'DELETE', 'User', pk, f'Пользователь {user.email} удалён')
    messages.success(request, 'Пользователь успешно удален.')
    return redirect('admin_user_list')

@login_required
def admin_user_restore(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    log_action(request.user, 'RESTORE', 'User', pk, f'Пользователь {user.email} восстановлен')
    messages.success(request, 'Пользователь успешно восстановлен.')
    return redirect('admin_user_list')

@login_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            log_action(request.user, 'EDIT', 'User', pk, f'Данные пользователя {user.email} обновлены')
            messages.success(request, 'Данные пользователя успешно обновлены.')
            return redirect('admin_user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin_db/user_edit.html', {'form': form, 'user': user})

@login_required
def admin_user_create(request):
    if not request.user.role or request.user.role.role_name != 'Администратор':
        messages.error(request, 'У вас нет прав для создания пользователей.')
        return redirect('admin_user_list')

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            log_action(request.user, 'CREATE', 'User', new_user.pk, f'Пользователь {new_user.email} создан')
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('admin_user_list')
        else:
            messages.error(request, 'Произошла ошибка при создании пользователя.')
    else:
        form = AdminUserCreationForm()

    return render(request, 'admin_db/user_create.html', {'form': form})
