from datetime import date, timedelta
from users.models import User
from books.models import BookCopy
from django.db import models


class Loan(models.Model):
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='loans')
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Заём копии {self.copy.book.title} пользователем {self.reader}"

    def get_status(self):
        if self.return_date:
            return "Завершённый"
        elif date.today() > self.due_date:
            return "Просроченный"
        else:
            return "Активный"


class ReservationStatuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.status_name


class Reservation(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    reservation_end_date = models.DateField()
    status = models.ForeignKey(ReservationStatuses, on_delete=models.CASCADE)

    def __str__(self):
        return f"Бронирование {self.copy} для {self.reader}"