import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def slow_signal_receiver(sender, instance, created, **kwargs):
    print("Signal started...")
    time.sleep(5)
    print("Signal finished!")


def trigger_user_creation():
    print("Before creating user")
    User.objects.create_user(username="testuser")
    print("After creating user and signal finishes")
