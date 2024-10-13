"""signal module form accounts"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import emails
from .models import Employee

User = get_user_model()


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, *args, **kwargs):
    """signal to create a new employee automatically when the user is created."""
    if created:
        try:
            emails.send_register_welcome(
                instance,
                instance.email,
                settings.COMPANY_NAME,
                settings.COMPANY_NAME,
                action_url="http://localhost:8000/login",
                login_url="http://localhost:8000/login",
                project_website="www.lavabwe.com",
            )
        except Exception as e:
            print("Error sending email for new user:", e)
        Employee.objects.create(user=instance)
