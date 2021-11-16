# Generated by Django 2.2.5 on 2021-11-16 13:59

from django.db import migrations, models
import time


class Migration(migrations.Migration):

    dependencies = [
        ('math_questions', '0002_auto_20211114_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qid', models.BigIntegerField()),
                ('label_id', models.BigIntegerField()),
                ('updated_at', models.IntegerField(default=time.time)),
                ('created_at', models.IntegerField(default=time.time)),
            ],
            options={
                'verbose_name': '知识点标记',
                'verbose_name_plural': '知识点标记',
            },
        ),
    ]
