from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class UsersProfile(AbstractUser):
    """Модель для хранения данных о пользователе."""

    username = None

    phone_number = models.CharField(
        verbose_name='Телефон спортивной школы',
        max_length=14,
        unique=True,
        validators=[
            MinLengthValidator(14, message='Минимум 14 символов'),
        ],
        blank=False
    )
    invite_code = models.CharField(
        verbose_name='Инвайт код пользователя',
        max_length=6,
        blank=True,
        null=True
    )
    auth_code = models.CharField(
        verbose_name='Инвайт код другого пользователя',
        max_length=6,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self) -> str:
        return self.phone_number
