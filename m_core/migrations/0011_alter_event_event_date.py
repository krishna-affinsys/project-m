# Generated by Django 3.2.2 on 2022-10-31 05:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("m_core", "0010_alter_event_event_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_date",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 10, 31, 5, 59, 26, 15742, tzinfo=utc)
            ),
        ),
    ]