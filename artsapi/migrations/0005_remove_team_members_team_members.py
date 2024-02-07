# Generated by Django 5.0.1 on 2024-02-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_department'),
        ('artsapi', '0004_team_share_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to='accounts.profile'),
        ),
    ]
