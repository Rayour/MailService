from mail.servises import MailService
from django.core.management import call_command
from django.core.management.base import BaseCommand
from mail.models import Newsletter
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Start newsletter from user'

    def add_arguments(self, parser):

        parser.add_argument('newsletter_id', type=int, help='ID рассылки')
        parser.add_argument('user_id', type=int, help='ID пользователя')

    def handle(self, *args, **kwargs):

        newsletter_id = kwargs['newsletter_id']
        user_id = kwargs['user_id']

        try:
            newsletter = Newsletter.objects.get(id=newsletter_id)
        except Exception as e:
            self.stdout.write(self.style.SUCCESS(f'Incorrect input: {e}'))
        else:
            try:
                user = CustomUser.objects.get(id=user_id)
            except Exception as e:
                self.stdout.write(self.style.SUCCESS(f'Incorrect input: {e}'))
            else:
                MailService.send_email(newsletter, user)
                self.stdout.write(self.style.SUCCESS('Newsletter started'))
