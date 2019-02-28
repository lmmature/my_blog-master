# Generated by Django 2.1.3 on 2018-11-28 04:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='T_title',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一标识')),
                ('title', models.CharField(blank=True, max_length=50, verbose_name='标题')),
                ('type_id', models.IntegerField(verbose_name='类型编码')),
                ('time', models.TimeField(verbose_name='录入时间')),
            ],
        ),
    ]
