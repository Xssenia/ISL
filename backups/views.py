from django.shortcuts import render, redirect
import subprocess

def create_backup(request):
    if request.method == 'POST':
        # Команда для создания бэкапа
        command = ["pg_dump", "-U", "your_db_user", "-F", "c", "-f", "backup_file_path", "your_database_name"]
        subprocess.run(command)
        return redirect('backup_list')
    return render(request, 'backups/create_backup.html')

def restore_backup(request):
    if request.method == 'POST':
        # Команда для восстановления бэкапа
        command = ["pg_restore", "-U", "your_db_user", "-d", "your_database_name", "-c", "backup_file_path"]
        subprocess.run(command)
        return redirect('backup_list')
    return render(request, 'backups/restore_backup.html')
