from rest_framework import viewsets

from .models import MetodoPago, Caja, Venta
from .serializers import MetodoPagoSerializer, CajaSerializer, VentaSerializer


class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer


class CajaViewSet(viewsets.ModelViewSet):
    queryset = Caja.objects.all()
    serializer_class = CajaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.prefetch_related('detalles').all()
    serializer_class = VentaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)