# Generated by Django 3.1.9 on 2021-06-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joha', '0003_paperversion_comment_to_reviewer'),
    ]

    operations = [
        migrations.CreateModel(
            name='JohaEventSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='추가된 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정된 일시')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='삭제된 일시')),
                ('receipt_start_at', models.DateTimeField(verbose_name='이벤트 시작일')),
                ('receipt_end_at', models.DateTimeField(verbose_name='이벤트 종료일')),
            ],
            options={
                'verbose_name': 'JOHA 이벤트 일정',
                'verbose_name_plural': 'JOHA 이벤트 일정',
            },
        ),
    ]
