# Generated by Django 3.2.7 on 2021-09-27 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visstability', '0009_auto_20210924_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcasenodes',
            name='activestep',
            field=models.BooleanField(default=False, help_text='Активный шаг тест-кейса', verbose_name='activestep'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='type_gr',
            field=models.CharField(choices=[('metric', 'метрика'), ('or', 'ИЛИ'), ('and', 'И'), ('true', 'единица'), ('service', 'сервис')], help_text='Тип вершины графа', max_length=10, verbose_name='type'),
        ),
    ]