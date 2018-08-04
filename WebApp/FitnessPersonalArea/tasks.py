import datetime
import random

from celery.task import periodic_task
from celery.schedules import crontab

from WebApp.celery import app

"""
celery -A WebApp worker -B  -l info
"""