from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.conf import settings
import os

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Nodes, Edges, TestCaseNodes
from .grstead import GStead, grput_model, grget_model, steptest_model

FILE_MODEL = 'monstability_model.xml'

class TestCaseNodesResource(resources.ModelResource):
    """Класс для импорта тест-кейса"""

    class Meta:
        model = TestCaseNodes
        fields = ('id', 'id_gr', 'access', 'stead', 'costdown', 'RTO', 'RPO',)

class NodesResource(resources.ModelResource):
    """Класс для импорта Nodes"""

    class Meta:
        model = Nodes
        fields = ('id', 'id_gr', 'type_gr', 'label_gr', 'layer', 'access', 'stead', 'costdown', 'coordX', 'coordY',
                  'RTO', 'RPO', 'color')

class EdgesResource(resources.ModelResource):
    """Класс для импорта Edges"""

    class Meta:
        model = Edges
        fields = ('id', 'id_gr', 'source', 'target', 'weight', 'color')

# классы панели админисратора
@admin.register(Nodes)
class NodesAdmin(ImportExportModelAdmin):
    resource_class = NodesResource
    list_display = ('id', 'id_gr', 'label_gr', 'type_gr', 'layer', 'access', 'stead', 'costdown', 'color',)
    list_filter = ('type_gr', 'layer',)
    list_display_links = ('id_gr',)
    actions = ['grload_model', 'grsave_model', 'grcalc_model', 'grcalc_costdown', 'grcalc_RTORPO']

    def changelist_view(self, request, extra_context=None):
        ''' эмуляция выбора всех элементов списка '''

        if 'action' in request.POST and request.POST['action'] in ('grload_model', 'grsave_model', ):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Nodes.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(ImportExportModelAdmin, self).changelist_view(request, extra_context)

    def grload_model(self, request, queryset):
        ''' загрузка графа из файла GEXF '''
        gr = GStead()
        gr.read_gexf(os.path.join(settings.STATIC_DIR, FILE_MODEL))
        grput_model(gr.G)
    grload_model.short_description = 'Загрузить модель из GEXF файла'

    def grsave_model(self, request, queryset):
        ''' сохранение графа в файл GEXF '''
        gr = GStead()
        grget_model(gr.G)
        gr.write_gexf(os.path.join(settings.STATIC_DIR, FILE_MODEL))
    grsave_model.short_description = 'Сохранить модель в GEXF файл'

    def grcalc_model(self, request, queryset):
        ''' пересчет показателей устойчивости '''
        gr = GStead()
        grget_model(gr.G)
        for node in queryset:
            gr.calc_node_stead(node_id=node.id_gr)
        grput_model(gr.G)
    grcalc_model.short_description = 'Пересчитать показатели'

    def grcalc_costdown(self, request, queryset):
        ''' пересчет показателей доступности '''
        gr = GStead()
        grget_model(gr.G)
        for node in queryset:
            gr.calc_costdown(node_id=node.id_gr)
        grput_model(gr.G)
    grcalc_costdown.short_description = 'Пересчитать стоимость простоя'

    def grcalc_RTORPO(self, request, queryset):
        ''' пересчет показателей RTO, RPO '''
        gr = GStead()
        grget_model(gr.G)
        for node in queryset:
            gr.calc_RTORPO(node_id=node.id_gr)
        grput_model(gr.G)
    grcalc_RTORPO.short_description = 'Пересчитать RTO и RPO'


@admin.register(Edges)
class EdgesAdmin(ImportExportModelAdmin):
    resource_class = EdgesResource
    list_display = ('id_gr', 'source', 'target', 'weight', 'color',)
    list_display_links = ('id_gr', 'source',)
#    list_filter = ('source', 'target',)


# from django.urls import path
# from django.utils.decorators import method_decorator
# from django.views.decorators.http import require_POST

@admin.register(TestCaseNodes)
class TestCaseNodesAdmin(ImportExportModelAdmin):
    resource_class = TestCaseNodesResource
    list_display = ('id', 'step', 'id_gr', 'activestep', 'access', 'stead', 'costdown', 'RTO', 'RPO',)
    list_display_links = ('id_gr',)
    actions = ['steptest',]
    # change_list_template = 'change_list.html'

    def changelist_view(self, request, extra_context=None):
        ''' эмуляция выбора всех элементов списка '''

        if 'action' in request.POST and request.POST['action'] in ('steptest',):
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Nodes.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(ImportExportModelAdmin, self).changelist_view(request, extra_context)

    # def get_urls(self):
    #     urls = super().get_urls()
    #     info = self.get_model_info()
    #     my_urls = [
    #         path('steptest/',
    #              # self.admin_site.admin_view(self.steptest),
    #              self.steptest,
    #              name='steptest',
    #              ),
    #     ]
    #     return my_urls + urls

    # @method_decorator(require_POST)
    def steptest(self, request=None, queryset=None):
        ''' выполняет шаг теста и устанавливает следующий '''
        steptest_model()
    steptest.short_description = "Выполнить очередной шаг теста"