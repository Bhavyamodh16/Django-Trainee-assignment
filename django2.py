# --- ADD THESE LINES TO THE VERY TOP OF django2.py ---
import os
import sys
import threading
import django


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def verify_thread_receiver(sender, instance, created, **kwargs):
    signal_thread_id = threading.current_thread().ident
    print(f"Signal Thread ID: {signal_thread_id}")

def trigger_user_creation():
    caller_thread_id = threading.current_thread().ident
    print(f"Caller Thread ID: {caller_thread_id}")
    
   
    User.objects.filter(username="testuser").delete()
    
    User.objects.create_user(username="testuser")

if __name__ == "__main__":
    trigger_user_creation()
