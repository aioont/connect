# Generated by Django 4.2.1 on 2023-06-16 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_connect_for_friendshiprequest_connect_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends_count',
            field=models.IntegerField(default=0),
        ),
    ]
