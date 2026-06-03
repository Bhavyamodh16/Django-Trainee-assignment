# --- ADD THESE LINES TO THE VERY TOP OF django3.py ---
import os
import sys
import django

# Tell Python where your project root folder is
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Tell Django where your settings file is
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
# Initialize Django applications
django.setup()
# -----------------------------------------------------

# Now it is safe to import Django and app modules
from django.db import transaction, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from myapp.models import Log

@receiver(post_save, sender=User)
def signal_db_operation(sender, instance, created, **kwargs):
    Log.objects.create(message=f"User {instance.username} saved.")
    print("Log created in signal.")

def create_user_within_transaction():
    # Cleanup previous entries from past runs
    User.objects.filter(username="testuser").delete()
    Log.objects.all().delete()
    
    try:
        with transaction.atomic():
            User.objects.create_user(username="testuser")
            print("Forcing a manual rollback exception...")
            raise IntegrityError("Forcing rollback to test transaction")
    except IntegrityError:
        print("Transaction rolled back successfully.")
        
        # Verify if log exists
        log_count = Log.objects.filter(message="User testuser saved.").count()
        print(f"Log count in database: {log_count} (Should be 0 if rolled back)")

if __name__ == "__main__":
    create_user_within_transaction()
