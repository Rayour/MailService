from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete groups and load groups from fixture'

    def handle(self, *args, **kwargs):

        Group.objects.all().delete()

        call_command('loaddata', 'groups_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded groups from fixture'))
