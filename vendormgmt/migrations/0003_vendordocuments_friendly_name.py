# Generated by Django 3.2.2 on 2021-06-06 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendormgmt', '0002_vendordocuments'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendordocuments',
            name='friendly_name',
            field=models.CharField(default='Friendly Name', max_length=200),
            preserve_default=False,
        ),
    ]
