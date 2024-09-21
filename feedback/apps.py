'''This file contains the configuration for the Django app named 'feedback'.
AppConfig subclasses define settings and behavior for the app within the Django project.
'''

from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'
