# Generated by Django 4.2 on 2023-04-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imageURL',
            field=models.URLField(max_length=300),
        ),
    ]
