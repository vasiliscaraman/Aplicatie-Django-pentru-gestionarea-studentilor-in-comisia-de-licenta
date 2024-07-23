# Generated by Django 4.2.4 on 2024-07-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='last_button_clicked',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='nota',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='status_inscriere',
        ),
        migrations.AddField(
            model_name='customuser',
            name='nota1',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nota2',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='customuser',
            name='notaFinala',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]
