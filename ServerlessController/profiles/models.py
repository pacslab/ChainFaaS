from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from pytz import timezone
from MSc_Research_Django.settings import TIME_ZONE


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    ready = models.BooleanField(default=False)
    last_ready_signal = models.DateTimeField(default=datetime(2018, 7, 1, tzinfo=timezone(TIME_ZONE)))
    location = models.CharField(max_length=30, blank=True)
    fabric_org = models.CharField(max_length=30, blank=True)
    ram = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def is_contributing(self):
        if self.active and self.ready:
            if self.last_ready_signal > datetime.now(timezone(TIME_ZONE)) - timedelta(minutes=1):
                return True
            else:
                return False
        else:
            return False


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Provider.objects.create(user=instance)
        Developer.objects.create(user=instance)
    instance.provider.save()
    instance.developer.save()
