# Generated by Django 3.1.5 on 2021-03-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20210228_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='anonymous_author',
            field=models.BooleanField(default=False, verbose_name='익명 여부'),
        ),
    ]
