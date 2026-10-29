from rest_framework import viewsets

from .models import Cliente, Credito, Abono, ComprobantePago, AcuerdoPago, EstadoCuenta
from .serializers import (
    ClienteSerializer, CreditoSerializer, AbonoSerializer,
    ComprobantePagoSerializer, AcuerdoPagoSerializer, EstadoCuentaSerializer,
)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer


class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = ComprobantePago.objects.all()
    serializer_class = ComprobantePagoSerializer


class AcuerdoPagoViewSet(viewsets.ModelViewSet):
    queryset = AcuerdoPago.objects.all()
    serializer_class = AcuerdoPagoSerializer


class EstadoCuentaViewSet(viewsets.ModelViewSet):
    queryset = EstadoCuenta.objects.all()
    serializer_class = EstadoCuentaSerializer