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
    try:
        with transaction.atomic():
            User.objects.create_user(username="testuser")
            raise IntegrityError("Forcing rollback to test transaction")
    except IntegrityError:
        print("Transaction rolled back.")
