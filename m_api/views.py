from django.shortcuts import render
from m_api.serializers import CustomerSerializer, AccountSerializer, CardSerializer
from rest_framework import viewsets
from m_core.models import Customer, Account, Card


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
