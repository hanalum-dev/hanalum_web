# Generated by Django 3.1.9 on 2021-06-13 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20210610_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likeactivity',
            options={'verbose_name': '좋아요/싫어요', 'verbose_name_plural': '좋아요/싫어요'},
        ),
        migrations.AlterModelOptions(
            name='viewhistory',
            options={'verbose_name': '조회 기록', 'verbose_name_plural': '조회 기록'},
        ),
    ]
