# Generated by Django 5.0.1 on 2024-05-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_appuser_groups_appuser_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('data', models.JSONField(default=dict, null=True)),
                ('time', models.DateTimeField(blank=True, default='1970-01-01 12:00:00')),
            ],
        ),
    ]
