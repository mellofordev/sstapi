# Generated by Django 5.0.1 on 2024-02-06 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(choices=[('CS', 'CS'), ('AM', 'CL'), ('BT', 'BT'), ('ECA', 'ECA'), ('ECB', 'ECB'), ('MEA', 'Mech A'), ('MEB', 'Mech B'), ('MA', 'Auto'), ('MP', 'MP'), ('default', 'default')], default='default', max_length=7),
        ),
    ]