from m_core.utils import batch_send_sms
from project_m.celery import app

# TODO: Create an event table (festivals, events and more)
@app.task(bind=True)
def schedule_event(self, *args):
    phone_numbers = args[1]
    batch_send_sms(phone_numbers, args[0])


# TODO: Implement monthly report
