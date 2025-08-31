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
