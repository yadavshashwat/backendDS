# Generated by Django 3.2.2 on 2021-06-06 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmgmt', '0004_vendoritem'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
