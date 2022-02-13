from rest_framework import serializers
from .models import Currency, Transaction, User

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields=('symbol','name','decimals')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('wallet', 'type', 'amount')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'alias', 'password', 'email')