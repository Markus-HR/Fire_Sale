# Generated by Django 4.0.4 on 2022-05-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_payments_card_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='card_no',
            field=models.BigIntegerField(),
        ),
    ]