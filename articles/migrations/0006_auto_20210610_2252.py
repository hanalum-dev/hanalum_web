# Generated by Django 3.1.9 on 2021-06-10 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0006_auto_20210610_2252'),
        ('articles', '0005_article_viewed_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='글쓴이'),
        ),
        migrations.AlterField(
            model_name='article',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='boards.board', verbose_name='게시판'),
        ),
        migrations.AlterField(
            model_name='articleattachment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='articles.article'),
        ),
    ]