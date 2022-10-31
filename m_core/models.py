import datetime

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone

from m_core.utils import send_sms, batch_send_sms
from m_core.tasks import schedule_event

def generate_account_id():
    acc_id = get_random_string(length=settings.ACC_NO_LEN, allowed_chars="1234567890")
    if Account.objects.filter(account_number=acc_id).exists():
        generate_account_id()
    return acc_id


def generate_customer_id():
    cif = get_random_string(length=settings.CIF_LEN, allowed_chars="1234567890")
    if Customer.objects.filter(customer_id=cif).exists():
        generate_customer_id()
    return cif


def generate_card_number():
    card_number = get_random_string(length=16, allowed_chars="1234567890")
    if Card.objects.filter(card_number=card_number).exists():
        generate_card_number()
    return card_number


# ====================================== Models =========================================


class Customer(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    customer_id = models.BigIntegerField(primary_key=True, unique=True, default=0)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_gender = models.CharField(max_length=1, choices=GENDER)
    customer_phone = models.CharField(max_length=15, unique=True)
    customer_address = models.CharField(max_length=100)
    customer_city = models.CharField(max_length=100)
    customer_state = models.CharField(max_length=100)
    customer_country = models.CharField(max_length=100)
    customer_dob = models.DateField()

    def __str__(self):
        return str(self.customer_id)


class Account(models.Model):
    ACCOUNT_TYPE = (
        ("P", "Personal"),
        ("B", "Business"),
    )
    ACCOUNT_STATUS = (
        ("A", "Active"),
        ("I", "Inactive"),
        ("C", "Closed"),
        ("B", "Blocked"),
    )
    account_number = models.BigIntegerField(unique=True, primary_key=True, default=0)
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE, default="P")
    account_status = models.CharField(max_length=1, choices=ACCOUNT_STATUS, default="A")
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_open_date = models.DateField(auto_now_add=True)
    account_close_date = models.DateField(null=True, blank=True)
    account_transfer_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=100000.00
    )
    account_withdrawal_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=50000.00
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="accounts"
    )

    def __str__(self):
        return str(self.account_number)


class Card(models.Model):
    CARD_TYPE = (
        ("C", "Credit"),
        ("D", "Debit"),
    )

    card_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=1, choices=CARD_TYPE, default="D")
    card_status = models.CharField(max_length=1)
    card_created = models.DateTimeField(auto_now_add=True)
    card_expiry = models.DateField()
    card_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return str(self.id)


class TransactionRecord(models.Model):
    TRANSACTION_STATUS = (
        ("S", "Success"),
        ("F", "Failed"),
    )

    TRANSACTION_TYPE = (
        ("D", "Deposit"),
        ("W", "Withdrawal"),
        ("T", "Transfer"),
    )

    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_description = models.CharField(max_length=100)
    transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS)
    transaction_sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transaction_sender"
    )
    transaction_receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transaction_receiver"
    )

    def __str__(self):
        return str(self.id)


class Offer(models.Model):
    OFFER_STATUS = (
        ("A", "Active"),
        ("I", "Inactive"),
    )

    OFFER_TYPE = (
        ("L", "Loan"),
        ("I", "Insurance"),
        ("C", "Credit Card"),
    )

    offer_name = models.CharField(max_length=100)
    offer_description = models.CharField(max_length=250)
    offer_status = models.CharField(max_length=1, choices=OFFER_STATUS, default="A")
    offer_type = models.CharField(max_length=1, choices=OFFER_TYPE, default="L")
    offer_created = models.DateTimeField(auto_now_add=True)
    offer_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Event(models.Model):
    event_title = models.CharField(max_length=400)
    event_description = models.CharField(max_length=250)
    event_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)

# ======================================Signal Methods =========================================


@receiver(signals.post_save, sender=Account)
def notify_account_creation(sender, instance, created, **kwargs):
    if created:
        # if new account was made, then set id and notify the customer.
        if instance.account_number == 0:
            instance.account_number = generate_account_id()
            instance.save()
            send_sms(
                instance.customer.customer_phone,
                f"Thank you for creating a new bank account with us. Your account number is {instance.account_number}, "
                f"and your current balance is Rs. {instance.account_balance}",
            )
        Account.objects.filter(account_number=0).delete()


@receiver(signals.post_save, sender=Customer)
def set_unique_customer_id(sender, instance, created, **kwargs):
    if created:
        if instance.customer_id == 0:
            instance.customer_id = generate_customer_id()
            instance.save()


def check_balance(sender, amount):
    return True if sender.account_balance >= amount else False


@receiver(signals.pre_save, sender=TransactionRecord)
def pre_check_transaction_and_transact(sender, instance, **kwargs):
    # NOTE: doesn't satisfy the edge case where account doesn't exist or is closed, please add the implementation soon.
    sen = instance.transaction_sender
    rec = instance.transaction_receiver

    if not check_balance(instance.transaction_sender, instance.transaction_amount):
        instance.transaction_status = "F"
        send_sms(
            sen.customer.customer_phone,
            f"We have received your request and the transaction has failed due to insufficient funds "
            f"in your account. Your balance was not debited.",
        )
    else:
        sen.account_balance -= instance.transaction_amount
        rec.account_balance += instance.transaction_amount

        sen.save()
        rec.save()

        instance.transaction_status = "S"

        send_sms(
            sen.customer.customer_phone,
            f"Rs. {instance.transaction_amount} was debited from your account {sen.account_number},  "
            f"as per your request. If the transaction was not made by you then please reach out to us "
            f"on our support channel.",
        )
        send_sms(
            rec.customer.customer_phone,
            f"Rs. {instance.transaction_amount} was credited to your account {rec.account_number}.",
        )


@receiver(signals.post_save, sender=TransactionRecord)
def alert_on_low_bal(sender, instance, created, **kwargs):
    sen = instance.transaction_sender
    if sen.account_balance < settings.MIN_BALANCE:
        send_sms(
            sen.customer.customer_phone,
            f"ALERT: You have only Rs. {sen.account_balance} in your account "
            f"{sen.account_number}, lower than the minimum balance.",
        )


@receiver(signals.post_save, sender=Offer)
def alert_on_offer(sender, instance, created, **kwargs):
    if instance.offer_status == "A":
        phone_numbers = list(
            Customer.objects.all().values_list("customer_phone", flat=True)
        )
        batch_send_sms(phone_numbers, instance.offer_description)

from datetime import datetime
import time

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

@receiver(signals.post_save, sender=Event)
def schedule_event(sender, instance, created, **kwargs):
    if created:
        phone_number = list(Customer.objects.all().values_list("customer_phone", flat=True))
        schedule_event.apply_async(args = [instance.event_description, phone_number], eta=datetime_from_utc_to_local(instance.event_date))

# ====================================== User pull services =========================================


def get_balance_request(mobile_number, account_number):
    bal = Account.objects.get(account_number=account_number).account_balance
    send_sms(mobile_number, f"You're current account balance is Rs. {bal}")


def get_account_status(mobile_number, account_number):
    status = Account.objects.get(account_number=account_number).account_status
    send_sms(
        mobile_number,
        f"Thank you for reaching out to us, your account is currently {status}",
    )


def request_cheque(mobile_number, account_number):
    # TODO: add a RequestService table where the customer's requested services are stored
    send_sms(
        mobile_number,
        f"We have received your request to dispatch a new cheque book for the "
        f"account {account_number}. Your request will be processed soon.",
    )


def request_card(account_number, card_type="D"):
    Card.objects.create(
        card_account=Account.objects.get(account_number=account_number),
        card_status="I",
        card_expiry=datetime.datetime.now() + datetime.timedelta(days=365),
        card_number=generate_card_number(),
        card_type=card_type,
    )
    customer_phone = Account.objects.get(
        account_number=account_number
    ).customer.customer_phone
    send_sms(
        customer_phone,
        f"We have received your request for a {card_type} card for the account {account_number}."
        f"The new card will be dispatched to your address after further processing.",
    )
