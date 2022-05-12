# Generated by Django 4.0.4 on 2022-05-12 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='item_picture',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=9999)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.items')),
            ],
        ),
    ]
