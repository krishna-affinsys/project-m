# Generated by Django 4.1.2 on 2022-10-31 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("m_core", "0008_alter_customer_customer_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_title", models.CharField(max_length=400)),
                ("event_description", models.CharField(max_length=250)),
                ("event_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
