from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.utils import timezone
from .models import Log
from users.models import User


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

BACKUP_DIR = os.path.join("admin_panel", "backups")

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

            # Создание резервной копии через команду dumpdata
            os.system(f"python manage.py dumpdata > {backup_file}")

            # Логируем действие
            Log.objects.create(
                user=request.user,
                type="SAVE_DB",
                entity="Database",
                entityID=0,
                action_details=f"База данных сохранена в файл: {backup_file}"
            )

            messages.success(request, f'База данных успешно сохранена в файл: {backup_file}')
        except Exception as e:
            messages.error(request, f'Ошибка при сохранении базы данных: {str(e)}')

    # При GET-запросе просто отображаем страницу
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
            # Сохранение загруженного файла
            backup_path = default_storage.save(f"admin_panel/backups/{backup_file.name}", backup_file)

            # Восстановление базы данных через loaddata
            os.system(f"python manage.py loaddata {backup_path}")

            # Логируем действие
            Log.objects.create(
                user=request.user,
                type="RESTORE_DB",
                entity="Database",
                entityID=0,
                action_details=f"База данных восстановлена из файла: {backup_file.name}"
            )

            messages.success(request, f'База данных успешно восстановлена из файла: {backup_file.name}.')
        except Exception as e:
            messages.error(request, f'Ошибка при восстановлении базы данных: {str(e)}')

    return render(request, 'admin_db/backup_restore.html')























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
