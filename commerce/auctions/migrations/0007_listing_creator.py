# Generated by Django 4.2 on 2023-04-09 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]