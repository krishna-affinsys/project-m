# Generated by Django 3.2.2 on 2022-10-31 05:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("m_core", "0009_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_date",
            field=models.DateTimeField(
                default=datetime.datetime(2022, 10, 31, 5, 58, 35, 165635)
            ),
        ),
    ]
