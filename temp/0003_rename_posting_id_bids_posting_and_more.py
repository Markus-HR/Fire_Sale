# Generated by Django 4.0.4 on 2022-05-09 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0002_alter_bids_user_id_alter_ratings_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='posting_id',
            new_name='posting',
        ),
        migrations.RenameField(
            model_name='bids',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='postings',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='ratings',
            old_name='posting_id',
            new_name='posting',
        ),
        migrations.RenameField(
            model_name='ratings',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='postings',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
