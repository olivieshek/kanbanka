from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Kanban(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название канбана',
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name='kanbans',
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Канбан"
        verbose_name_plural = "Канбаны"


class Task(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название задачи',
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание задачи',
        blank=True,
    )
    # FIXME дефолт при миграции
    kanban = models.ForeignKey(
        Kanban,
        verbose_name='Канбан',
        related_name='task_kanban',
        on_delete=models.CASCADE,
        choices=User.kanbans
    )
    STATUSES = (
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
    )
    status = models.CharField(
        max_length=100,
        choices=STATUSES,
    )
    owner = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True,
    )
    creation_date = models.DateField(auto_now_add=True,)
    creation_time = models.TimeField(auto_now_add=True,)
    assigned_date = models.DateField(blank=True, default=timezone.now,)
    assigned_time = models.TimeField(blank=True, default=timezone.now,)
    executor = models.ForeignKey(
        User,
        verbose_name="Исполнитель",
        related_name='task_owner',
        null=True,
        on_delete=models.SET_NULL,
    )
    planned_date = models.DateField(blank=True, default=timezone.now,)
    planned_time = models.TimeField(blank=True, default=timezone.now,)
    completed_date = models.DateField(blank=True, default=timezone.now,)
    completed_time = models.TimeField(blank=True, default=timezone.now,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
