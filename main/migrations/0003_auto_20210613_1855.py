# Generated by Django 3.1.9 on 2021-06-13 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210429_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainboard',
            options={'verbose_name': '메인화면 게시판', 'verbose_name_plural': '메인화면 게시판'},
        ),
        migrations.AlterModelOptions(
            name='topbanner',
            options={'verbose_name': '탑배너', 'verbose_name_plural': '탑배너'},
        ),
    ]