from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Имя",
                                  help_text="Необязательное поле. Введите Ваше имя")
    last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Фамилия",
                                 help_text="Необязательное поле. Введите Вашу фамилию")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Аватар",
                               help_text="Необязательное поле. Загрузите изображение для Вашего профиля")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Телефон",
                                    help_text="Необязательное поле. Введите Ваш номер телефона")
    country = models.CharField(max_length=30, null=True, blank=True, verbose_name="Страна",
                               help_text="Необязательное поле. Укажите Вашу страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        """Строковое представление пользователя"""

        return self.email
