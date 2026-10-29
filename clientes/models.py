from django.conf import settings
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=30, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Credito(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('pagado', 'Pagado'), ('vencido', 'Vencido')]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='creditos')
    venta = models.OneToOneField('ventas.Venta', on_delete=models.PROTECT, related_name='credito')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Crédito #{self.pk} - {self.cliente} (saldo {self.saldo})"


class Abono(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.PROTECT, related_name='abonos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey('ventas.MetodoPago', on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    observacion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Abono #{self.pk} - {self.monto}"


class ComprobantePago(models.Model):
    ESTADOS = [('vigente', 'Vigente'), ('anulado', 'Anulado')]

    abono = models.OneToOneField(Abono, on_delete=models.PROTECT, related_name='comprobante')
    numero_comprobante = models.CharField(max_length=30, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    observacion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='vigente')

    def __str__(self):
        return self.numero_comprobante


class AcuerdoPago(models.Model):
    ESTADOS = [('activo', 'Activo'), ('cumplido', 'Cumplido'), ('incumplido', 'Incumplido')]

    credito = models.ForeignKey(Credito, on_delete=models.PROTECT, related_name='acuerdos')
    fecha_acuerdo = models.DateField()
    monto_acordado = models.DecimalField(max_digits=12, decimal_places=2)
    numero_cuotas = models.PositiveIntegerField()
    valor_cuota = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=12, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Acuerdo #{self.pk} - Crédito {self.credito_id}"


class EstadoCuenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='estados_cuenta')
    fecha_corte = models.DateField()
    saldo_anterior = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_creditos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_abonos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cliente} - corte {self.fecha_corte}"
