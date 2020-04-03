from django.db import models
from profiles.models import Developer, User, Provider
from developers_app.models import Services
from datetime import datetime
from pytz import timezone
from MSc_Research_Django.settings import TIME_ZONE


# Create your models here.
class Job(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime(2018, 7, 1, tzinfo=timezone(TIME_ZONE)))
    ack_time = models.DateTimeField(default=datetime(2018, 7, 1, tzinfo=timezone(TIME_ZONE)))
    pull_time = models.IntegerField(default=0)
    run_time = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    cost = models.FloatField(default=0.0)
    finished = models.BooleanField(default=False)