# Generated by Django 4.2.4 on 2024-07-03 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customuser_rejection_reason_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incarcarepdf',
            name='rejection_reason',
        ),
    ]