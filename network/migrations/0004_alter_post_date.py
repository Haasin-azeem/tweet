# Generated by Django 4.1.7 on 2023-03-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Date',
            field=models.CharField(default='today', max_length=300),
        ),
    ]
