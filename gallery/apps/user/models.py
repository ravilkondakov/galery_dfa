from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ()

    username = None
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$"
    )
    phone = models.CharField(
        validators=[phoneNumberRegex],
        max_length=16,
        unique=True
    )
    avatar = models.ImageField(
        blank=True,
        upload_to='images/avatar'
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
        blank=False
    )
    address = models.CharField(
        verbose_name='address',
        max_length=150,
        blank=False
    )
    email = models.EmailField()

    password = models.CharField(
        verbose_name='password',
        max_length=200,
        blank=False
    )

    def __str__(self):
        return f'User: {self.phone}'

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    @property
    def jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    @property
    def jwt_refresh_token(self):
        refresh = RefreshToken.for_user(self)

        return str(refresh)

    class Meta:
        ordering = ('-id', 'first_name', 'last_name')
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
