from django.conf import settings
from django.db import models
from django.utils import timezone


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Caja(models.Model):
    ESTADOS = [('abierta', 'Abierta'), ('cerrada', 'Cerrada')]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='abierta')

    def __str__(self):
        return f"Caja #{self.pk} ({self.estado})"


class Venta(models.Model):
    ESTADOS = [('pagada', 'Pagada'), ('credito', 'A crédito'), ('anulada', 'Anulada')]

    cliente = models.ForeignKey('clientes.Cliente', null=True, blank=True,
                                on_delete=models.PROTECT, related_name='ventas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT, related_name='ventas')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pagada')

    def __str__(self):
        return f"Venta #{self.pk} - {self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"