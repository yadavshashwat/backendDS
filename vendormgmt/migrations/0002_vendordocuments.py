# Generated by Django 3.2.2 on 2021-06-06 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendormgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('path', models.CharField(max_length=200)),
                ('file_name', models.CharField(max_length=200)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendormgmt.vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]