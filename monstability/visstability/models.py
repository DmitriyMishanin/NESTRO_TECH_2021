"""
    'AutoField', 'BLANK_CHOICE_DASH', 'BigAutoField', 'BigIntegerField',
    'BinaryField', 'BooleanField', 'CharField', 'CommaSeparatedIntegerField',
    'DateField', 'DateTimeField', 'DecimalField', 'DurationField',
    'EmailField', 'Empty', 'Field', 'FieldDoesNotExist', 'FilePathField',
    'FloatField', 'GenericIPAddressField', 'IPAddressField', 'IntegerField',
    'NOT_PROVIDED', 'NullBooleanField', 'PositiveIntegerField',
    'PositiveSmallIntegerField', 'SlugField', 'SmallAutoField',
    'SmallIntegerField', 'TextField', 'TimeField', 'URLField', 'UUIDField',
"""
from django.db import models

class Nodes(models.Model):
    """ вершины графа устойчивости"""

    NODES_TYPE = [
        ('metric', 'метрика'),
        ('or', 'ИЛИ'),
        ('and', 'И'),
        ('true', 'единица'),
        ('service', 'сервис'),
    ]
    LAYER_TYPE = [
        ('it', 'ИТ-ресурс'),
        ('bs', 'Бизнес-система'),
        ('bu', 'Бизнес-услуга'),
        ('br', 'Бизнес-решение'),
        ('bp', 'Бизнес-процесс'),
        ('ot', 'Прочее'),
    ]
    id_gr= models.CharField('idgr',
                            help_text='id вершины',
                            max_length=10,
                            )
    label_gr = models.CharField('label',
                                help_text='Название вершины',
                                max_length=250,
                                )
    type_gr = models.CharField('type',
                               help_text='Тип вершины графа',
                               max_length=10,
                               choices=NODES_TYPE,
                               )
    layer = models.CharField('layer',
                              help_text='Бизнес-слой',
                              max_length=4,
                              choices=LAYER_TYPE,
                              )
    access = models.IntegerField('access',
                                 help_text='Доступность',
                                 default=1,
                                 )

    stead = models.FloatField('stead',
                              help_text='Устойчивость',
                              default=1,
                              )
    costdown = models.FloatField('costdown',
                                 help_text='Стоимость простоя',
                                 default=1,
                                 )
    coordX = models.IntegerField('X',
                                 help_text='Координата X',
                                 default=1,
                                 )
    coordY = models.IntegerField('Y',
                                 help_text='Координата Y',
                                 default=1,
                                 )
    RTO = models.IntegerField('RTO',
                              help_text='Время, в течении которого узел может оставаться недоступным',
                              default=1,
                              )
    RPO = models.IntegerField('RPO',
                              help_text='Максимальный период времени, за который могут быть потеряны данные узла',
                              default=1,
                              )
    color = models.CharField('color',
                             help_text='Цвет',
                             max_length=100,
                             default='red',
                             )

    def pos(self):
        return f"{self.coordX:d} {self.coordY:d}"

    def description(self):
        result = f"{self.label_gr}\n" \
               f"Доступность: {self.access}\n" \
               f"Устойчивость: {self.stead*100:.2f} %"
        if self.type_gr != 'metric':
            result += f"\nСтоим.простоя (в сут.): {self.costdown:,.2f} руб.\n" \
               f"RTO: {self.RTO} ч\n" \
               f"RPO: {self.RPO} ч"
        print(f"{self.type_gr=}")
        return result

    def icon(self):
        return f"{self.layer}_{self.type_gr}"

    def __str__(self):
        return f"{self.label_gr} ({self.id_gr})"

    class Meta:
        verbose_name = 'Вершина графа устойчивости'
        verbose_name_plural = 'Вершины графа устойчивости'

class Edges(models.Model):
    """ ребра графа устойчивости"""

    id_gr= models.CharField('idgr',
                            help_text='id ребра',
                            max_length=10,
                            )
    source = models.CharField('source',
                              help_text='Верхина начало',
                              max_length=10,
                              )
    target = models.CharField('target',
                                help_text='Вершина конец',
                                max_length=10,
                                )
    weight = models.FloatField('weight',
                               help_text='Весм вершины',
                               default=1,
                               )
    color = models.CharField('color',
                             help_text='Цвет',
                             max_length=100,
                             default='red',
                             )
    def __str__(self):
        return f"({self.source}) - ({self.source})"

    class Meta:
        verbose_name = 'Ребро графа устойчивости'
        verbose_name_plural = 'Ребра графа устойчивости'


class TestCaseNodes(models.Model):
    """ данные для тестирования измнения параметров узлов"""

    id_gr = models.CharField('idgr',
                             help_text='id вершины',
                             max_length=10,
                             )
    step = models.IntegerField('step',
                              help_text='Шаг теста',
                              default=1,
                              )
    access = models.IntegerField('access',
                                 help_text='Доступность',
                                 default=1,
                                 blank=True,
                                 null=True,
                                 )

    stead = models.FloatField('stead',
                              help_text='Устойчивость',
                              default=1,
                              blank=True,
                              null=True,
                              )
    costdown = models.FloatField('costdown',
                                 help_text='Стоимость простоя',
                                 default=1,
                                 blank=True,
                                 null=True,
                                 )
    RTO = models.IntegerField('RTO',
                              help_text='Время, в течении которого узел может оставаться недоступным',
                              default=1,
                              blank=True,
                              null=True,
                              )
    RPO = models.IntegerField('RPO',
                              help_text='Максимальный период времени, за который могут быть потеряны данные узла',
                              default=1,
                              blank=True,
                              null=True,
                              )
    activestep = models.BooleanField('activestep',
                              help_text='Активный шаг тест-кейса',
                              default=False,
                              )

    def __str__(self):
        return f"{self.id_gr})"

    class Meta:
        verbose_name = 'Запись тестового примера'
        verbose_name_plural = 'Записи показателей метрик тестового примера'
