# Generated by Django 4.2.1 on 2023-06-15 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_friends_friendshiprequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendshiprequest',
            old_name='connect_with',
            new_name='connect_for',
        ),
    ]
