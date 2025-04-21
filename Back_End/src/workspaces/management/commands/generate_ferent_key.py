from django.core.management.base import BaseCommand , CommandError
from cryptography.fernet import Fernet
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Generate a FERENT_KEY to put in .env file"

    def handle(self, *args, **options):
        self.stdout.write(f'\n{Fernet.generate_key().decode()}')
        # print(f'\n{Fernet.generate_key().decode()}')
        self.stdout.write(f'\nPlease place the generated FERENT_KEY in your .env file')
        # print(f'\nPlease place the generated FERENT_KEY in your .env file')