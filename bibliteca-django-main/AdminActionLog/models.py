from django.db import models
from django.contrib.auth.models import User
from library.models import Book  # Certifique-se de que o app `library` está instalado

class AdminActionLog(models.Model):
    ACTION_CHOICES = [
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    ]

    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    reason = models.TextField(null=True, blank=True)  # Opcional para rejeição
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_user.username} - {self.action} - {self.book.title}"
