# Generated by Django 3.2.2 on 2021-05-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=100)),
                ('owner_name', models.CharField(max_length=100)),
                ('owner_phone', models.IntegerField()),
                ('contact_name', models.CharField(max_length=100, null=True)),
                ('contact_phone', models.IntegerField(null=True)),
                ('email', models.CharField(max_length=150, null=True)),
                ('city', models.CharField(max_length=150, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('source', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
