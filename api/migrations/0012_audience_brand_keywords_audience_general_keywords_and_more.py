# Generated by Django 5.1.4 on 2024-12-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_audience_audience_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='audience',
            name='brand_keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audience',
            name='general_keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audience',
            name='lifestyle',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audience',
            name='media_habits',
            field=models.TextField(blank=True, null=True),
        ),
    ]
