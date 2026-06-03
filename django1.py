import os
import sys
import time
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def slow_signal_receiver(sender, instance, created, **kwargs):
    print("Signal started...")
    time.sleep(5)  # This will block execution
    print("Signal finished!")

def trigger_user_creation():
    print("Before creating user")
    

    User.objects.filter(username="testuser").delete()
    
    User.objects.create_user(username="testuser")
    print("After creating user and signal finishes")

if __name__ == "__main__":
    trigger_user_creation()
