# Generated by Django 5.1.3 on 2024-12-05 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_customuser_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
