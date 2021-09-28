"""
Модуль расчета устойчивости и формирования сигналов отклонений
Допущения:
    Граф устойчивости направленный.
    Обход графа начинается с узлов метрик.
    Ребра имеют веса.

Ограничения:
    Узлы графа содержат атрибуты:
        'type':string - тип узла
            'metric' - узел метрики
            'service' - узел сервиса
            'and' - узел логического И
            'or' - узел логического ИЛИ
            'true' - узел единичной функции (доступность всегда 1)
        'access':integer - текущая доступность
        'stead':float - текущая устойчивость
        'costdown':float - текущая стоимость простоя
    Ребра графа содержат свойство:
        'weight':float - вес ребра (коэффициент передачи сигнала)
    Узлы типа 'metric', 'service', 'true' могут иметь только одно входящее ребро
"""

import networkx as nx
from django.db import transaction

from .models import Nodes, Edges, TestCaseNodes

TYPE_METRIC = 'metric'
TYPE_SERVICE = 'service'
TYPE_AND = 'and'
TYPE_OR = 'or'

COLOR_GOOT = 'green'
COLOR_WAR = 'orange'
COLOR_ERR = 'red'

class GStead:
    """ Класс графа устойчивости """

    G = None    # граф класса

    def __init__(self):
        self.G = nx.DiGraph()


    def read_gexf(self, path):
        """ загрузка графа из файла GEXF """
        self.G = nx.read_gexf(path)


    def write_gexf(self, path):
        """ выгрузка графа в файла GEXF """
        nx.write_gexf(self.G, path)


    def calc_node_stead(self, node_id):
        """ пересчет устойчивости узла """

        edge_list = list(nx.edge_bfs(self.G, node_id))  # обход в ширину для узла node
        for u, v in edge_list:  # перебор всех ребер текущего узла
            self._calc_stead(node_id=v)     # расчитываем устойчивость узла на конце ребра
            self._calc_access(node_id=v)    # расчитываем доступность узла на конце ребра


    def calc_RTORPO(self, node_id):
        """ функция расчета RTO, RPO в зависимых узлах"""
        lst_out_edges = list(self.G.out_edges(node_id)) # список исходящих ребер
        if len(lst_out_edges) > 0:    # обновление RTO, RPO текущего узла если у него есть входящие ребра
            minRTO = self.G.nodes[lst_out_edges[0][1]]['RTO']
            minRPO = self.G.nodes[lst_out_edges[0][1]]['RPO']
            for u, v in lst_out_edges:
                if self.G.nodes[v]['RTO'] < minRTO:
                    minRTO = self.G.nodes[v]['RTO']  # минимальное значение RTO исходящих узлов
                if self.G.nodes[v]['RPO'] < minRPO:
                    minRPO = self.G.nodes[v]['RPO']  # минимальное значение RPO исходящих узлов

            self.G.nodes[node_id]['RTO'] = minRTO
            self.G.nodes[node_id]['RPO'] = minRPO

        lst_in_edges = list(self.G.in_edges(node_id))  # список входящих ребер
        for u, v in lst_in_edges:   # рекурсивный вызов расчета для узлов входящих ребер
            self.calc_RTORPO(u)


    def calc_costdown(self, node_id):
        """ функция расчета стоимости простоя в зависимых узлах"""

        lst_out_edges = list(self.G.out_edges(node_id)) # список исходящих ребер
        if len(lst_out_edges) > 0:    # обновление стоимости простоя текущего узла если у него есть входящие ребра
            costdown = 0
            for u, v in lst_out_edges:
                if self.G.nodes[v]['type'] == TYPE_OR:
                    costdown += self.G.nodes[v]['costdown'] * self.G[u][v]['weight']  # ИЛИ сумма делится в соответствии с весами
                else:
                    costdown += self.G.nodes[v]['costdown'] # для остальных И сумма равна для всех узлов

            self.G.nodes[node_id]['costdown'] = costdown

        lst_in_edges = list(self.G.in_edges(node_id))  # список входящих ребер
        for u, v in lst_in_edges:   # рекурсивный вызов расчета для узлов входящих ребер
            self.calc_costdown(u)


    def calc_metrics_stead(self):
        """ пересчет устойчивости по всем нодам метрик"""

        nodesid_metric = []  # список узлов с метриками
        for node in self.G.nodes.data():    # обход по вершинам графа
            if node[1]['type'] == TYPE_METRIC:    # если тип ноды 'metric'
                nodesid_metric.append(node[0])   # добавляем id ноды в список узлов метрик

        for node_id in nodesid_metric:
            self.calc_node_stead(node_id)   # выполняем расчет с обходом в ширину по всем узлам метрик


    def _calc_stead(self, node_id):
        """ функция расчета устойчивости ноды """

        lst_in_edges = list(self.G.in_edges(node_id))   # список входящих ребер
        stead = 0;
        for u,v in lst_in_edges:
            stead += self.G.nodes[u]['stead'] * self.G[u][v]['weight']  # сумма устойчивости входящих узлов умноженный на вес ребра
        self.G.nodes[node_id]['stead'] = stead  # обновление устойчивости текущего узла

    def _calc_access(self, node_id):
        """ функция расчета доступности ноды """
        lst_in_edges = list(self.G.in_edges(node_id))   # список входящих ребер
        access = 1;
        for u,v in lst_in_edges:
            if self.G.nodes[v]['type'] == TYPE_OR:
                access = access or self.G.nodes[u]['access']    # ИЛИ доступностей входящих узлов
            else:
                access = access and self.G.nodes[u]['access']   # И доступностей входящих узлов для других узлов
        self.G.nodes[node_id]['access'] = access  # обновление доступности текущего узла


# функции работы с моделью
def grget_model(AG):
    ''' загрузка графа из базы данных '''
    qrND = Nodes.objects.all()
    for ND in qrND:
        AG.add_node(
            ND.id_gr,
            type=ND.type_gr,
            label=ND.label_gr,
            layer=ND.layer,
            access=ND.access,
            stead=ND.stead,
            costdown=ND.costdown,
            coordX=ND.coordX,
            coordY=ND.coordY,
            RTO=ND.RTO,
            RPO=ND.RPO,
            color=ND.color,
        )
    qrNE = Edges.objects.all()
    for NE in qrNE:
        AG.add_edge(
            NE.source,
            NE.target,
            weight=NE.weight,
            id=NE.id_gr,
            color=NE.color,
        )

def get_color(access, stead):
    ''' получить цвет узла '''
    if not access or stead < 0.6:
        return COLOR_ERR
    elif stead < 0.9:
        return COLOR_WAR
    else:
        return COLOR_GOOT

def grput_model(AG):
    ''' выгрузка графа в базу данных '''
    if len(AG) > 0:
        Nodes.objects.all().delete()
        for node in AG.nodes.data():
            nodecolor = get_color(node[1]['access'], node[1]['stead'])
            ND = Nodes.objects.create(
                id_gr=node[0],
                label_gr=node[1]['label'],
                type_gr=node[1]['type'],
                layer=node[1]['layer'],
                access=node[1]['access'],
                stead=node[1]['stead'],
                costdown=node[1]['costdown'],
                coordX=node[1]['coordX'],
                coordY=node[1]['coordY'],
                RTO=node[1]['RTO'],
                RPO=node[1]['RPO'],
                # color=node[1]['color'],
                color=nodecolor,
            )
            ND.save()

        Edges.objects.all().delete()
        for edge in AG.edges.data():
            edgecolor = get_color(AG.nodes.data()[edge[0]]['access'], AG.nodes.data()[edge[0]]['stead'])
            NE = Edges.objects.create(
                source=edge[0],
                target=edge[1],
                id_gr=edge[2]['id'],
                weight=edge[2]['weight'],
                # color=edge[2]['color'],
                color=edgecolor,
            )
            NE.save()

def steptest_model():
    ''' выполняет шаг теста и устанавливает следующий '''

    result = {}
    qrTC = TestCaseNodes.objects.all().order_by('step')
    TC = qrTC[0]
    for i in range(qrTC.count()):
        if qrTC[i].activestep:
            TC = qrTC[i]
            try:
                TCnext = qrTC[i+1]
            except:
                TCnext = qrTC[0]
            break

    try:
        ND = Nodes.objects.get(id_gr=TC.id_gr)
    except:
        print(f"error: Nodes.objects.get(id_gr={TC.id_gr})")
    else:
        with transaction.atomic():
            # заполнение ревизитов
            if not TC.access is None:
                ND.access = TC.access
            if not TC.stead is None:
                ND.stead = TC.stead
            if not TC.costdown is None:
                ND.costdown = TC.costdown
            if not TC.RTO is None:
                ND.RTO = TC.RTO
            if not TC.RPO is None:
                ND.RPO = TC.RPO
            ND.save()

            # персчет показателей
            gr = GStead()
            grget_model(gr.G)
            gr.calc_node_stead(node_id=TC.id_gr)
            gr.calc_costdown(node_id=TC.id_gr)
            gr.calc_RTORPO(node_id=TC.id_gr)
            grput_model(gr.G)

            # изменение шага
            TC.activestep = False
            TC.save()
            TCnext.activestep = True
            TCnext.save()

            result = {
                'step':TC.step,
                'id_gr':TC.id_gr,
            }


    return result


if __name__ == '__main__':
    pass
