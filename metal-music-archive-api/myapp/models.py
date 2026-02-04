from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass

class Band(models.Model):
    name = models.CharField(max_length=50, null=False)
    genre = models.CharField(max_length=50)
    formed_year = models.IntegerField()
    origin_country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"

class Album(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField()
    release_date = models.IntegerField()
    order_number = models.PositiveIntegerField(auto_created=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')
    


class Track(models.Model):
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    order_number = models.PositiveIntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')