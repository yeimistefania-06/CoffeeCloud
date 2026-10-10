from django.db import models

class categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class producto(models.Model):
    categoria = models.ForeignKey(categoria, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)

def __str__(self):
    return self.nombre
