from data_base import db_model
from data_base.db_controller import get_all_some, get_impact_types_by_dev_id, get_ubi_by_dev_id, get_negative_by_dev_id, \
    get_realization_by_dev_id, get_vul_by_dev_id, get_scenario_by_dev_id_threat_id, get_ip
from py_ui.ui_EngineerWindow import Ui_EngineerWindow
from PyQt5 import QtWidgets
from functions import functions, threat_model
from view.admin_window import AdminWindow
from functions import scenario_attack
from PyQt5.QtGui import QPixmap, QIcon


class EngineerWindow(QtWidgets.QMainWindow, Ui_EngineerWindow):
    def __init__(self, engine):
        try:
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Инженер ИБ')
            self.setWindowIcon(QIcon('files/open_lock.ico'))
            self.engine = engine

            self.devices_parsed = {}
            self.devices = []
            self.dev_selected = db_model.DeviceBase

            self.impact = []
            self.impact_parsed = {}
            self.impact_all = []
            self.impact_all_parsed = {}
            self.impact_selected = db_model.ImpactTypeBase

            self.ubi = []
            self.ubi_parsed = {}
            self.ubi_all = []
            self.ubi_all_parsed = {}
            self.ubi_selected = db_model.ThreatBase

            self.negative = []
            self.negative_parsed = {}
            self.negative_all = []
            self.negative_all_parsed = {}
            self.negative_selected = db_model.NegativeResultBase

            self.vul = []
            self.vul_parsed = {}
            self.vul_all = []
            self.vul_all_parsed = {}
            self.vul_selected = db_model.VulnerabilityBase

            self.realization = []
            self.realization_parsed = {}
            self.realization_all = []
            self.realization_all_parsed = {}
            self.realization_selected = db_model.RealizationWayBase

            self.scenario = []
            self.scenario_parsed = {}
            self.scenario_all = []
            self.scenario_all_parsed = {}
            self.scenario_selected = db_model.DeviceScenarioBase

            self.modeling_btn.setEnabled(False)
            self.modeling_btn.clicked.connect(self.modeling_page_show)
            self.guidebook_btn.clicked.connect(self.guidebook_show)
            self.scenario_btn.clicked.connect(self.scenario_page_show)
            self.threat_model_btn.clicked.connect(self.threat_model_create)
            self.template_btn.clicked.connect(self.template_page_show)

            self.scenario_get_btn.clicked.connect(self.scenario_get_btn_pressed)
            self.modeling_page_show()

            self.threat_list.itemSelectionChanged.connect(self.threat_list_selected)
        except Exception as e:
            print(e)

    def template_page_show(self):
        self.all_btn_enable()
        self.stackedWidget.setCurrentWidget(self.template_page)
        self.template_btn.setEnabled(False)

    def threat_model_create(self):
        threat_model.create_threat_model(self.engine)

    def scenario_page_show(self):
        self.all_btn_enable()
        self.stackedWidget.setCurrentWidget(self.scenario_page)
        self.scenario_btn.setEnabled(False)

    def scenario_get_btn_pressed(self):
        try:
            all_connections = get_all_some(self.engine, db_model.DeviceConnectionBase)
            con_array = []
            for i in all_connections:
                con_array.append((i.first_device_id, i.second_device_id))
            scenario_attack.do_scenario(con_array, int(self.first_le.text()), int(self.second_le.text()))
            # scene = QtWidgets.QGraphicsScene(self)
            # pixmap = QPixmap('functions/scenario_attack_output/graph[1, 4, 5].png')
            # item = QtWidgets.QGraphicsPixmapItem(pixmap)
            # scene.addItem(item)
            # self.graphicsView.setScene(scene)
            pixmap = QPixmap("functions/scenario_attack_output/graph[1, 4, 5, 7].png")  # Путь к вашему изображению
            self.picture.setPixmap(pixmap)

            # Включение масштабирования изображения
            self.picture.setScaledContents(True)
        except Exception as e:
            print(e)

    def guidebook_show(self):
        admin_window = AdminWindow(self.engine)
        self.guide_page = admin_window
        self.guide_page.show()

    def modeling_page_show(self):
        self.all_btn_enable()
        self.stackedWidget.setCurrentWidget(self.modeling_page)
        self.modeling_btn.setEnabled(False)
        self.devices_parsed.clear()
        devices = get_all_some(self.engine, db_model.DeviceBase)
        for i in devices:
            ips = get_ip(self.engine, i.id)
            string_ip = ''
            for ip in ips:
                string_ip += ip.ip_address + ' '
            self.devices.append(f'{i.id} | {string_ip}')
            self.devices_parsed[f'{i.id} | {string_ip}'] = i
        self.device_list.addItems(self.devices)
        self.device_list.itemSelectionChanged.connect(self.device_list_selected)

    def all_btn_enable(self):
        self.modeling_btn.setEnabled(True)
        self.scenario_btn.setEnabled(True)
        self.template_btn.setEnabled(True)

    def device_list_selected(self):
        try:
            a = self.device_list.selectedItems()[0].text()
            self.dev_selected = self.devices_parsed[a]

            self.impact_parsed.clear()
            self.impact = get_impact_types_by_dev_id(self.engine, self.dev_selected.id)
            print(self.impact)
            impact = []
            for i in self.impact:
                impact.append(f'{i[1]}')
                self.impact_parsed[f'{i[1]}'] = i
            self.impact = impact
            self.impact_list.addItems(self.impact)

            self.ubi_parsed.clear()
            self.ubi = get_ubi_by_dev_id(self.engine, self.dev_selected.id)
            ubi = []
            for i in self.ubi:
                ubi.append(f'УБИ.{str(functions.beautify_ubi(i[0]))} {i[1]}')
                self.ubi_parsed[f'УБИ.{str(functions.beautify_ubi(i[0]))} {i[1]}'] = i
            self.ubi = ubi
            self.threat_list.addItems(self.ubi)

            self.negative_parsed.clear()
            self.negative = get_negative_by_dev_id(self.engine, self.dev_selected.id)
            negative = []
            for i in self.negative:
                negative.append(f'{i[1]}')
                self.negative_parsed[f'{i[1]}'] = i
            self.negative = negative
            self.negative_result_cb.addItems(self.negative)
            # add all

            self.realization_parsed.clear()
            self.realization = get_realization_by_dev_id(self.engine, self.dev_selected.id)
            realization = []
            for i in self.realization:
                realization.append(f'{i[1]}')
                self.realization_parsed[f'{i[1]}'] = i
            self.realization = realization
            self.realization_way_list.addItems(self.realization)

            self.vul_parsed.clear()
            self.vul = get_vul_by_dev_id(self.engine, self.dev_selected.id)
            vul = []
            for i in self.vul:
                vul.append(f'{i[1]} | {i[2]}')
                self.vul_parsed[f'{i[1]} | {i[2]}'] = i
            self.vul = vul
            self.vulnerability_list.addItems(self.vul)
        except Exception as e:
            print(e)

    def threat_list_selected(self):
        a = self.threat_list.selectedItems()[0].text()
        self.ubi_selected = self.ubi_parsed[a]
        self.tactic_technique_list.clear()

        self.scenario_parsed.clear()
        self.scenario = get_scenario_by_dev_id_threat_id(self.engine, self.dev_selected.id, self.ubi_selected[0])
        scenario = []
        for i in self.scenario:
            scenario.append(f'T{i[-2]}.{i[-1]} {i[-3]}')
            self.scenario_parsed[f'T{i[-2]}.{i[-1]} {i[-3]}'] = i
        self.scenario = scenario
        self.tactic_technique_list.addItems(self.scenario)
