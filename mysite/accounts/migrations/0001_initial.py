# Generated by Django 4.2.4 on 2023-09-04 08:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254)),
                ('nume', models.CharField(blank=True, max_length=30, null=True)),
                ('initiala_tatalui', models.CharField(max_length=1)),
                ('prenume', models.CharField(blank=True, max_length=50, null=True)),
                ('numar_telefon', models.CharField(blank=True, max_length=100, null=True)),
                ('rol', models.CharField(choices=[('Student', 'Student'), ('Secretar', 'Secretar'), ('Membru comisie', 'Membru Comisie')], default='Student', max_length=20)),
                ('este_inscris', models.BooleanField(default=False)),
                ('status_inscriere', models.CharField(choices=[('Aprobat', 'Aprobat'), ('Respins', 'Respins'), ('In asteptare', 'In Asteptare')], default='In asteptare', max_length=12)),
                ('nota', models.FloatField(default=0, max_length=2)),
                ('last_button_clicked', models.CharField(choices=[('modify1', 'Aprobat'), ('modify2', 'In Asteptare'), ('modify3', 'Respins')], default='modify2', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='IncarcarePDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titlul_lucrarii', models.CharField(max_length=100)),
                ('descrierea_lucrarii', models.TextField(max_length=3000)),
                ('nume_student', models.CharField(max_length=30)),
                ('initiala_tatalui', models.CharField(max_length=1)),
                ('prenume_student', models.CharField(max_length=50)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
