# Generated by Django 4.1.7 on 2023-03-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likedUsers',
            field=models.CharField(default=2, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
