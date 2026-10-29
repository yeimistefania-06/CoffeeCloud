from django.db import transaction
from rest_framework import serializers

from clientes.models import Credito
from .models import MetodoPago, Caja, Venta, DetalleVenta


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'


class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'
        read_only_fields = ['usuario']


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'descuento', 'subtotal']
        read_only_fields = ['subtotal']
        extra_kwargs = {'precio_unitario': {'required': False}}


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'usuario', 'caja', 'metodo_pago', 'fecha',
                  'subtotal', 'descuento', 'total', 'estado', 'detalles']
        read_only_fields = ['usuario', 'subtotal', 'total']

    def validate(self, data):
        if data.get('estado') == 'credito' and not data.get('cliente'):
            raise serializers.ValidationError('Una venta a crédito necesita un cliente.')
        if not data.get('detalles'):
            raise serializers.ValidationError('La venta debe tener al menos un producto.')
        return data

    @transaction.atomic
    def create(self, validated_data):
        detalles = validated_data.pop('detalles')
        descuento = validated_data.get('descuento', 0)
        venta = Venta.objects.create(**validated_data)

        subtotal = 0
        for item in detalles:
            producto = item['producto']
            cantidad = item['cantidad']
            if producto.stock_actual < cantidad:
                raise serializers.ValidationError(
                    f'Stock insuficiente de "{producto.nombre}" (hay {producto.stock_actual}).'
                )
            precio = item.get('precio_unitario', producto.precio_venta)
            desc = item.get('descuento', 0)
            sub = precio * cantidad - desc

            DetalleVenta.objects.create(
                venta=venta, producto=producto, cantidad=cantidad,
                precio_unitario=precio, descuento=desc, subtotal=sub,
            )
            producto.stock_actual -= cantidad
            producto.save(update_fields=['stock_actual'])
            subtotal += sub

        venta.subtotal = subtotal
        venta.total = subtotal - descuento
        venta.save(update_fields=['subtotal', 'total'])

        if venta.estado == 'credito':
            Credito.objects.create(
                cliente=venta.cliente, venta=venta,
                monto=venta.total, saldo=venta.total,
            )
        return venta