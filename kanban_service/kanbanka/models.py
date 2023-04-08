from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название задачи',
        unique=True,
    )
    text = models.TextField(
        max_length=1500,
        verbose_name='Описание задачи',
        blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',  # TODO нормальное название ему
        related_name='created_tasks',
        on_delete=models.SET_DEFAULT,
        default='non-existent user'
    )


class ActiveTask(models.Model):
    """
    author - user (creator), default
    actionee - user, designed by author
    start date
    deadline
    """
    author = models.ForeignKey(
        User,
        verbose_name='Автор',  # TODO нормальное название ему
        related_name='created_tasks',
        on_delete=models.SET_DEFAULT,
        default='non-existent user'
    )


class Desk(models.Model):
    ...


"""
user | done [2]
task
desk
"""
