# Generated by Django 4.0.4 on 2022-05-09 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_accounts", "0003_kanvasuser_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="kanvasuser",
            name="address",
        ),
    ]
