# Generated by Django 5.1.2 on 2024-11-03 15:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="expiringtoken",
            options={
                "verbose_name": "ExpiringToken",
                "verbose_name_plural": "ExpiringTokens",
            },
        ),
    ]