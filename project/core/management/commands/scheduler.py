# -*- coding: utf-8 -*-
from time import sleep

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            User.send_vehicle_number_nitification()
            sleep(60)
            # sleep(5)

