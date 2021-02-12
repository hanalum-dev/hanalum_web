# Generated by Django 3.1.5 on 2021-02-12 05:26

import django_summernote.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='제목')),
                ('content', django_summernote.fields.SummernoteTextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성된 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 날짜')),
            ],
        ),
    ]
