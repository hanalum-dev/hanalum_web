# Generated by Django 3.1.9 on 2021-06-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joha', '0002_auto_20210613_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperversion',
            name='comment_to_reviewer',
            field=models.TextField(blank=True, null=True, verbose_name='리뷰어에게 남기는 요청사항'),
        ),
    ]