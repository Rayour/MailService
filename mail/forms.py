from django import forms
from .models import Customer, Message, Newsletter


class CustomerForm(forms.ModelForm):
    """Класс формы создания/редактирования клиента"""

    class Meta:
        """Описание формы для создания/редактирования клиента"""

        model = Customer
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(CustomerForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["full_name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
        })


class MessageForm(forms.ModelForm):
    """Класс формы создания/редактирования письма"""

    class Meta:
        """Описание формы для создания/редактирования письма"""

        model = Message
        fields = ["topic", "text"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["topic"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["text"].widget.attrs.update({
            "class": "form-control",
        })


class NewsletterForm(forms.ModelForm):
    """Класс формы создания/редактирования рассылки"""

    class Meta:
        """Описание формы для создания/редактирования рассылки"""

        model = Newsletter
        fields = ["name", "message", "customers"]

    def __init__(self, *args, **kwargs):
        """Метод инициализации формы. Добавление стилизации"""

        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["message"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["customers"].widget.attrs.update({
            "class": "form-control",
        })
