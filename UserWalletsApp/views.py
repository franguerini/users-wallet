from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status

from UserWalletsApp.models import User, Currency, Transaction
from UserWalletsApp.serializers import UserSerializer, CurrencySerializer, TransactionSerializer


@csrf_exempt
def userApi(request, id = 0):
    # Returns a list of users when called
    # TODO: Add filtering
    if request.method=='GET':
        users = User.objects.all()
        usersSerializer = UserSerializer(users, many=True)
        return JsonResponse(usersSerializer.data, safe=False)

    # Creates a user and creates the default wallets
    elif request.method=='POST':
        userData=JSONParser().parse(request)
        usersSerializer=UserSerializer(data=userData)
        if usersSerializer.is_valid():
            usersSerializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(usersSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

    # TODO
    # elif request.method=='PUT':

    # TODO
    # elif request.method=='DELETE':

@csrf_exempt
def userBalancesApi(request):
    # Gets user balances for all of the users wallets
    if request.method=='GET':
        result = User.getUserBalances(user_id=request.GET["user_id"])
        if result['error']:
            return JsonResponse(result['message'], safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(result['balances'], safe=False)

@csrf_exempt
def userTransactionsApi(request):
    # Gets a list of all the transactions made by a user
    # TODO Add pagination, Add a serializer to validate and clean the parameters
    if request.method=='GET':
        result = User.getUserTransactions(params=request.GET)
        serializedTransactions = TransactionSerializer(result, many=True)
        return JsonResponse(serializedTransactions.data, safe=False)

@csrf_exempt
def currenciesApi(request):
    # Gets a list of the currencies
    if request.method=='GET':
        currencies = Currency.objects.all()
        currenciesSerializer = CurrencySerializer(currencies, many=True)
        return JsonResponse(currenciesSerializer.data, safe=False)

    # Creates a new currency
    elif request.method=='POST':
        currency_data=JSONParser().parse(request)
        currenciesSerializer = CurrencySerializer(data=currency_data)
        if currenciesSerializer.is_valid():
            currenciesSerializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)


@csrf_exempt
def transactionApi(request):
    # Executes a transaction on a user wallets
    if request.method=='POST':
        transactionData=JSONParser().parse(request)
        transactionSerializer = TransactionSerializer(data=transactionData)
        if transactionSerializer.is_valid():
            result = Transaction.executeTransaction(data=transactionData)
            if result['error']:
                return JsonResponse(result['message'], safe=False, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(result['message'], safe=False)
        return JsonResponse(transactionSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

