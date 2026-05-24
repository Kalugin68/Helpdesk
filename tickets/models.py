from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):

    class Status(models.TextChoices):
        NEW = 'NEW', 'Новая'
        IN_PROGRESS = 'IN_PROGRESS', 'В работе'
        DONE = 'DONE', 'Выполнена'
        REJECTED = 'REJECTED', 'Отклонена'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tickets',
        null = True,
        blank = True
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.title}"
