from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=40)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
