# Generated by Django 5.1.6 on 2025-03-05 11:42

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


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
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('age_range', models.CharField(choices=[('under_18', 'Under 18'), ('18_24', '18-24'), ('25_34', '25-34'), ('35_44', '35-44'), ('45_54', '45-54'), ('55_64', '55-64'), ('65_plus', '65+')], help_text='Select your age range.', max_length=10)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('non_binary', 'Non-binary'), ('prefer_not_to_say', 'Prefer not to say')], help_text='Select your gender.', max_length=20)),
                ('profession', models.CharField(help_text='Enter your profession.', max_length=100)),
                ('hobbies', models.TextField(help_text='List your hobbies, separated by commas.')),
                ('location', models.CharField(help_text='Enter your city or region.', max_length=100)),
                ('clothing_size', models.CharField(help_text='Enter your clothing size (e.g., S, M, L).', max_length=10)),
                ('preferred_style', models.CharField(help_text='Your preferred fashion style (e.g., casual, formal, bohemian).', max_length=100)),
                ('budget', models.CharField(help_text='Your typical budget for fashion items.', max_length=50)),
                ('favorite_colors', models.CharField(help_text='Your favorite colors, separated by commas.', max_length=100)),
                ('occasions', models.TextField(help_text='Occasions you shop for (e.g., work, casual, party).')),
                ('brand_preferences', models.TextField(help_text='Your favorite fashion brands.')),
                ('body_type', models.CharField(help_text='Share your body type.', max_length=50)),
                ('sustainability_preference', models.BooleanField(default=False, help_text='Check if you prefer eco-friendly fashion options.')),
                ('favorite_influencers', models.TextField(help_text='Names of fashion influencers you follow.')),
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
    ]
