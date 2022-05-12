# Generated by Django 4.0.4 on 2022-05-06 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("address", "0001_initial"),
        ("user_accounts", "0002_kanvasuser_is_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="kanvasuser",
            name="address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="address.address",
            ),
        ),
    ]
