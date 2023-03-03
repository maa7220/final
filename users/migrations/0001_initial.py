# Generated by Django 4.1.6 on 2023-02-08 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import users.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('role', models.CharField(max_length=30)),
                ('specialization', models.CharField(max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to=users.models.upload_to)),
                ('gender', models.CharField(max_length=100)),
                ('age', models.CharField(blank=True, max_length=3, null=True)),
                ('nat_id', models.IntegerField()),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_nurse', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users',
                'db_table': 'Users',
                'ordering': ['-date_joined'],
            },
        ),
    ]