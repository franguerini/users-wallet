from django.db import models
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class TransactionType(models.TextChoices):
    DEPOSIT = 'deposit', _('Deposit')
    WITHDRAWL = 'withdrawl', _('Withdrawl')

class TransactionStatus(models.TextChoices):
    FAILED = 'failed', _('Failed')
    SUCCESS = 'success', _('Success')


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    decimals = models.PositiveSmallIntegerField()
    createByDefault = models.BooleanField(default=False)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    # TODO: Password should be encripted
    password = models.CharField(max_length=50)

    # When a user is saved in the database it also checks if there are any
    # default databases that need to be created, if so, it creates them
    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            currencies = Currency.objects.filter(createByDefault=True)
            for currency in currencies:
                Wallet.objects.create(user=self, currency=currency)

    def getUserBalances(user_id):
        balances = []
        wallets = Wallet.objects.filter(user_id=user_id)
        if not wallets:
            return { 'error': True, 'message': f'No wallets found for user_id: {user_id}' }
        for wallet in wallets:
            try:
                currency = Currency.objects.get(id=wallet.currency_id)
            except Currency.DoesNotExist:
                return { 'error': True, 'message': f'Something went wrong, currency not found' }

            balances.append({ 'balance': wallet.balance, 'currency': currency.symbol })
        return { 'error': False, 'balances': balances }

    # TODO: Add pagination to this method
    def getUserTransactions(params):
        walletQuery = {}

        currencyId = params.get('currency_id')
        if currencyId:
            currency = Currency.objects.get(id=currencyId)
            if not currency:
                return { 'error': True, 'message': f'Invalid currency: {currencyId}' }
            walletQuery['currency'] = currency

        userId = params.get('user_id')
        if userId:
            walletQuery['user_id'] = userId

        wallets = Wallet.objects.filter(**walletQuery)
        if not wallets:
            return { 'error': True, 'message': f'No wallets found for user_id: {userId}' }

        query = {}
        query['wallet__in'] = wallets
        transactionType = params.get('type')
        if transactionType:
            query['type'] = transactionType

        transactions = Transaction.objects.filter(**query)
        return transactions


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def deposit(self, amount):
        self.balance = amount + self.balance
        self.save()
        return { 'error': False }

    def withdrawl(self, amount):
        if self.balance >= amount:
            self.balance = self.balance - amount
            self.save()
            return { 'error': False }
        else:
            return { 'error': True, 'message': 'Insufficient funds' }


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    status = models.CharField(max_length=10, choices=TransactionStatus.choices)

    def executeTransaction(data):
        wallet = Wallet.objects.get(id=data['wallet'])
        if not wallet:
            return { 'error': True, 'message': f'Wallet not found wallet id: {wallet}' }
        if data['type'] == TransactionType.DEPOSIT:
            result = wallet.deposit(amount=data['amount'])
        elif data['type'] == TransactionType.WITHDRAWL:
            result = wallet.withdrawl(amount=data['amount'])
        else:
            return { 'error': True, 'message': 'Invalid transaction type' }

        transaction = {}
        transaction['status'] = TransactionStatus.FAILED if result['error'] else TransactionStatus.SUCCESS
        transaction['wallet'] = wallet
        transaction['amount'] = data['amount']
        transaction['type'] = data['type']

        Transaction.objects.create(**transaction)

        response = {}
        response['error'] = True if result['error'] else False
        response['message'] = result['message'] if result['error'] else 'Transaction successfull'

        return response





