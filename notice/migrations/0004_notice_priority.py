# Generated by Django 3.1.5 on 2021-02-28 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_notice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='priority',
            field=models.IntegerField(default=0, verbose_name='우선순위'),
        ),
    ]
