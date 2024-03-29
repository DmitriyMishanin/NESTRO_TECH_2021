# Generated by Django 3.2.7 on 2021-09-27 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visstability', '0010_auto_20210927_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcasenodes',
            name='RPO',
            field=models.IntegerField(blank=True, default=1, help_text='Максимальный период времени, за который могут быть потеряны данные узла', null=True, verbose_name='RPO'),
        ),
        migrations.AlterField(
            model_name='testcasenodes',
            name='RTO',
            field=models.IntegerField(blank=True, default=1, help_text='Время, в течении которого узел может оставаться недоступным', null=True, verbose_name='RTO'),
        ),
        migrations.AlterField(
            model_name='testcasenodes',
            name='access',
            field=models.IntegerField(blank=True, default=1, help_text='Доступность', null=True, verbose_name='access'),
        ),
        migrations.AlterField(
            model_name='testcasenodes',
            name='costdown',
            field=models.FloatField(blank=True, default=1, help_text='Стоимость простоя', null=True, verbose_name='costdown'),
        ),
        migrations.AlterField(
            model_name='testcasenodes',
            name='stead',
            field=models.FloatField(blank=True, default=1, help_text='Устойчивость', null=True, verbose_name='stead'),
        ),
    ]
