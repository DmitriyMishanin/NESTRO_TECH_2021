# Generated by Django 3.2.7 on 2021-09-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visstability', '0007_testcasenodes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testcasenodes',
            options={'verbose_name': 'Запись тестового примера', 'verbose_name_plural': 'Записи показателей метрик тестового примера'},
        ),
        migrations.AlterField(
            model_name='nodes',
            name='RPO',
            field=models.IntegerField(default=1, help_text='Максимальный период времени, за который могут быть потеряны данные узла', verbose_name='RPO'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='RTO',
            field=models.IntegerField(default=1, help_text='Время, в течении которого узел может оставаться недоступным', verbose_name='RTO'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='access',
            field=models.IntegerField(default=1, help_text='Доступность', verbose_name='access'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='color',
            field=models.CharField(default='red', help_text='Цвет', max_length=100, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='coordX',
            field=models.IntegerField(default=1, help_text='Координата X', verbose_name='X'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='coordY',
            field=models.IntegerField(default=1, help_text='Координата Y', verbose_name='Y'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='costdown',
            field=models.FloatField(default=1, help_text='Стоимость простоя', verbose_name='costdown'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='stead',
            field=models.FloatField(default=1, help_text='Устойчивость', verbose_name='stead'),
        ),
    ]
