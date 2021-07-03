# Generated by Django 3.1.9 on 2021-07-03 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0010_normalboard'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NormalBoard',
        ),
        migrations.AlterField(
            model_name='board',
            name='type',
            field=models.CharField(blank=True, default='board', max_length=20, null=True, verbose_name='게시판 타입'),
        ),
    ]
