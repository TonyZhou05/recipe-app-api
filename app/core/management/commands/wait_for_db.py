"""
Django commands to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psychopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to wait for database"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database")

        db_up = False

        # keep trying until db_up is TRUE
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psychopg2OpError, OperationalError):
                self.stdout.write('Database not available, waiting 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database Available"))
