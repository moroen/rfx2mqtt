from django.db import models
from django.urls import reverse

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("ROOMS:detail", kwargs={"pk": self.id})
