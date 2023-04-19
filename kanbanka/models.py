from django.db import models
from django.contrib.auth.models import User


class Kanban(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название канбана',
    )
    # TODO: owner, date

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
        verbose_name='Автор',  # TODO нормальное название ему
        on_delete=models.SET_NULL,
        null=True,
    )
    assigned_date = models.DateField(blank=True)
    assigned_time = models.TimeField(blank=True)

#
#
# class ActiveTask(models.Model):
#     """
#     owner - user (creator), default
#     actionee - user, designed by owner
#     start date
#     deadline
#     """
#     author = models.ForeignKey(
#         User,
#         verbose_name='Автор',  # TODO нормальное название ему
#         related_name='created_activetasks',
#         on_delete=models.SET_DEFAULT,
#         default='non-existent user'
#     )
#
#
# """
# user | done [2]
# task
# desk
# """
