import os, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    args = '(none)'
    help = ''

    def handle(self, *args, **options):
        pass
