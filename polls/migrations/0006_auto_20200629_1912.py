# Generated by Django 2.2.10 on 2020-06-29 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_answer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('user_id', 'question')},
        ),
    ]