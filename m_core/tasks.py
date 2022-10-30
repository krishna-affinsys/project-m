from m_core.models import TransactionRecord, Account, Customer
from m_core.utils import batch_send_sms


# TODO: Create an event table (festivals, events and more)
def event(event_date="", event_message=""):
    phone_numbers = list(
        Customer.objects.all().values_list("customer_phone", flat=True)
    )
    batch_send_sms(phone_numbers, event_message)


# TODO: Implement monthly report
