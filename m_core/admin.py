from django.contrib import admin
from m_core.models import Account, Customer, Card, TransactionRecord, Offer, Event

admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Card)
admin.site.register(TransactionRecord)
admin.site.register(Offer)
admin.site.register(Event)
