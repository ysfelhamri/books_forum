"""
WSGI config for books_forum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
import threading
import time
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books_forum.settings')

application = get_wsgi_application()



def run_periodic_tasks():
    while True:
        call_command('update_book_stats')
        time.sleep(6 * 60 * 60 )  

if 'runserver' in sys.argv:
    threading.Thread(target=run_periodic_tasks, daemon=True).start()