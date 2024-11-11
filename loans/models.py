from users.models import User
from books.models import BookCopy
from django.db import models

class Loan(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.copy} выдан {self.reader}"

class Reservation(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    reservation_end_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Бронирование {self.copy} для {self.reader}"

