from django.contrib.auth.models import AbstractUser
from django.db import models

class rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nombre

class usuario(AbstractUser):
    rol = models.ForeignKey(rol, on_delete=models.PROTECT, null=True)