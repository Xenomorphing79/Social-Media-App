# Generated by Django 3.2 on 2021-04-20 15:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followers', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('followed_by', 'following')},
        ),
    ]
