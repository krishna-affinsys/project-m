# Generated by Django 4.1.2 on 2022-10-30 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("m_core", "0005_alter_account_account_number_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Offers",
            new_name="Offer",
        ),
    ]
