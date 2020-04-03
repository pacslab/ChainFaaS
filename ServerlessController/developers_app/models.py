from django.db import models
from profiles.models import Developer, User, Provider


# Create your models here.
class Services(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    docker_container = models.URLField()
    active = models.BooleanField(default=False)

    class Meta:
        # Each developer can only have one service with a specific name
        unique_together = ['name', 'developer']
