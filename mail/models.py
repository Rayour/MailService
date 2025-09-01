from django.db import models
from users.models import CustomUser


class Customer(models.Model):
    """Модель клиента (получателя писем)"""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True,
                               help_text="Вы можете оставить комментарий относительно клиента")
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="customers")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта клиента"""

        return self.email

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ["full_name"]
        permissions = [
            ('can_view_all', 'Can view all items'),
        ]


class Message(models.Model):
    """Модель сообщения"""

    topic = models.CharField(max_length=150, verbose_name="Тема письма", help_text="Укажите тему письма")
    text = models.TextField(verbose_name="Текст письма",
                            help_text="Введите текст письма")
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="messages")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта письма"""

        return self.topic

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"
        ordering = ["topic"]
        permissions = [
            ('can_view_all', 'Can view all items'),
        ]


class Newsletter(models.Model):
    """Модель рассылки"""

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    name = models.CharField(max_length=100, verbose_name="Название", help_text="Укажите название рассылки", default="Рассылка")
    message = models.ForeignKey(Message, verbose_name="Письмо", help_text="Выберите письмо для рассылки",
                                on_delete=models.CASCADE, related_name="newsletters")
    customers = models.ManyToManyField(Customer, verbose_name="Клиенты",
                                       help_text="Укажите клиентов для отправки письма")
    start_send_time = models.DateTimeField(verbose_name="Дата и время начала отправки писем", null=True, blank=True)
    finish_send_time = models.DateTimeField(verbose_name="Дата и время окончания отправки писем", null=True, blank=True)
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="newsletters")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта рассылки"""

        return self.status

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["start_send_time"]
        permissions = [
            ('can_view_all', 'Can view all items'),
            ('can_send_newsletters', 'Can send newsletters'),
        ]


class Attempt(models.Model):
    """Модель попытки отправки письма"""

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('fail', 'Не успешно'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    customer = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.CASCADE,
                                 related_name="attempts")
    message = models.ForeignKey(Message, verbose_name="Письмо", on_delete=models.CASCADE, related_name="attempts")
    server_response = models.TextField(verbose_name="Ответ сервера", null=True, blank=True)
    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="attempts")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    def __str__(self):
        """Строковое представление объекта попытки отправки"""

        return self.status

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
        permissions = [
            ('can_view_all', 'Can view all items'),
        ]
