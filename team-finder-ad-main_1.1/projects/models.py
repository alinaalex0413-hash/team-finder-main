from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("closed", "Закрыт"),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
        null=True,  # временно добавить
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default="open", verbose_name="Статус"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
