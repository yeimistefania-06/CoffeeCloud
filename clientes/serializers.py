from django.db import transaction
from rest_framework import serializers

from .models import Cliente, Credito, Abono, ComprobantePago, AcuerdoPago, EstadoCuenta


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'
        read_only_fields = ['saldo', 'estado']


class AbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abono
        fields = '__all__'
        read_only_fields = ['usuario']

    def validate(self, data):
        credito = data['credito']
        if credito.estado == 'pagado':
            raise serializers.ValidationError('Este crédito ya está pagado.')
        if data['monto'] <= 0:
            raise serializers.ValidationError('El monto debe ser mayor que cero.')
        if data['monto'] > credito.saldo:
            raise serializers.ValidationError(
                f'El abono supera el saldo pendiente ({credito.saldo}).'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        abono = super().create(validated_data)
        credito = abono.credito
        credito.saldo -= abono.monto
        if credito.saldo == 0:
            credito.estado = 'pagado'
        credito.save(update_fields=['saldo', 'estado'])
        return abono


class ComprobantePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobantePago
        fields = '__all__'


class AcuerdoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcuerdoPago
        fields = '__all__'


class EstadoCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCuenta
        fields = '__all__'