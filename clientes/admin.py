from django.contrib import admin
from .models import Cliente, Credito, Abono, ComprobantePago, AcuerdoPago, EstadoCuenta

admin.site.register(Cliente)
admin.site.register(Credito)
admin.site.register(Abono)
admin.site.register(ComprobantePago)
admin.site.register(AcuerdoPago)
admin.site.register(EstadoCuenta)