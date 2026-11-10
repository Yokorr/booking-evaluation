from django.db import models

class Location(models.Model):
    code = models.SlugField(max_length=12, primary_key=True)
    city = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.city

class Room(models.Model):
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    location = models.ForeignKey(Location, related_name='rooms', on_delete=models.PROTECT)

    def __str__(self):
        return self.code
