import os
import sys
import copy
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from data_base import db_model
import math
from data_base.db_controller import get_all_ubi, get_object_type_by_ubi_id, delete_threat_device_type, get_all_device_type, \
    create_some, get_all_negatives, delete_negative_by_id, delete_obj_type_by_id, get_interfaces_by_device_type_id, \
    get_all_interfaces, delete_interface_obj_type_by_id, get_realization_by_interface_id, get_all_realization_ways, \
    delete_interface_by_id, delete_interface_realization_way_by_id, delete_some_by_id, get_some_by_id, get_all_some, \
    get_connected_devices_by_id, update_some_by_id, delete_device_connection, get_worker_criteria, \
    delete_worker_criteria_by_id, get_technique_by_tac_id, get_vulnerabilities, get_vulnerability_type_by_vul_id, \
    get_vulnerability_software_by_vul_id, count_vulnerabilities, vulnerability_search, \
    delete_worker_insider_criteria_by_id, get_insider_criteria_type_by_ins_id, delete_insider_criteria_type, \
    delete_some_by_parameter, get_criteria_type, get_worker_insider_by_type_id, get_ip
from functions.functions import beautify_ubi, check_bool
from py_ui.ui_AdminWindow import Ui_AdminWindow


class AdminWindow(QtWidgets.QMainWindow, Ui_AdminWindow):
    def __init__(self, engine):
        try:
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Администратор ИБ')
            self.setWindowIcon(QIcon('files/open_lock.ico'))
            self.engine = engine
            #  threat_page
            self.threat_btn.clicked.connect(self.threat_page_show)
            self.threat_selected_ubi = ''
            self.threat_selected_obj = ''
            self.threat_get_ubi = ''
            self.threat_get_ubi_parsed = {}
            self.threat_get_object_type = ''
            self.threat_get_object_type_parsed = {}
            self.threat_get_all_object_type = ''
            self.threat_get_all_object_type_parsed = {}
            self.threat_change_mode = False
            self.threat_ubi_list.itemClicked.connect(self.threat_ubi_list_clicked)
            self.threat_object_list.itemSelectionChanged.connect(self.threat_object_list_selected)
            self.threat_object_add_btn.clicked.connect(self.threat_object_add_btn_clicked)
            self.threat_object_change_btn.clicked.connect(self.threat_object_change_btn_clicked)
            self.threat_object_delete_btn.clicked.connect(self.threat_object_delete_btn_clicked)
            #  negative_page
            self.negative_btn.clicked.connect(self.negative_page_show)
            self.negative_get_neg = ''
            self.negative_get_neg_parsed = {}
            self.negative_delete_btn.clicked.connect(self.negative_neg_list_delete)
            self.negative_add_btn.clicked.connect(self.negative_neg_list_add)
            self.negative_neg_list.itemSelectionChanged.connect(self.negative_neg_list_selected)
            self.negative_selected = db_model.NegativeResultBase
            # object_page
            self.object_btn.clicked.connect(self.object_page_show)
            self.object_object_list_select_item = db_model.DeviceTypeBase
            self.object_get_interface = ''
            self.object_get_interface_parsed = {}
            self.object_get_all_interface = ''
            self.object_get_all_interface_parsed = {}
            self.object_obj_list.itemSelectionChanged.connect(self.object_obj_list_selected)
            self.object_delete_btn.clicked.connect(self.object_obj_delete_btn_pressed)
            self.object_add_btn.clicked.connect(self.object_obj_add_btn_pressed)
            self.object_change_mode = False
            self.object_interface_selected = db_model.InterfaceBase
            self.object_interface_list.itemSelectionChanged.connect(self.object_interface_list_selected)
            self.object_change_interface_btn.clicked.connect(self.object_change_interface_btn_pressed)
            self.object_add_interface_btn.clicked.connect(self.object_add_interface_btn_pressed)
            self.object_delete_interface_btn.clicked.connect(self.object_delete_interface_btn_pressed)
            #  interface_page
            self.interface_btn.clicked.connect(self.interface_page_show)
            self.interface_int_list_selected = db_model.InterfaceBase
            self.interface_get_int = ''
            self.interface_get_int_parsed = {}
            self.interface_get_realization = ''
            self.interface_get_realization_parsed = {}
            self.interface_get_all_realization = ''
            self.interface_get_all_realization_parsed = {}
            self.interface_int_list.itemSelectionChanged.connect(self.interface_int_list_select)
            self.interface_delete_btn.clicked.connect(self.interface_int_delete_btn_pressed)
            self.interface_add_btn.clicked.connect(self.interface_int_add_btn_pressed)
            self.interface_change_mode = False
            self.interface_realization_selected = db_model.InterfaceBase
            self.interface_realization_list.itemSelectionChanged.connect(
                self.interface_realization_list_selected)
            self.interface_change_realization_btn.clicked.connect(self.interface_change_realization_btn_pressed)
            self.interface_add_realization_btn.clicked.connect(self.interface_add_realization_btn_pressed)
            self.interface_delete_realization_btn.clicked.connect(self.interface_delete_realization_btn_pressed)
            #  realization_page
            self.realization_btn.clicked.connect(self.realization_page_show)
            self.realization_real_list.itemSelectionChanged.connect(self.realization_real_list_selected)
            self.realization_delete_btn.clicked.connect(self.realization_delete_btn_pressed)
            self.realization_add_btn.clicked.connect(self.realization_add_btn_pressed)
            self.realization_real_selected = db_model.RealizationWayBase
            self.realization_get_real = ''
            self.realization_get_real_parsed = {}
            #  device_page
            self.device_btn.clicked.connect(self.device_page_show)
            self.device_dev_list.itemSelectionChanged.connect(self.device_dev_list_selected)
            self.device_delete_btn.clicked.connect(self.device_delete_btn_pressed)
            self.device_add_btn.clicked.connect(self.device_add_btn_pressed)
            self.device_change_dev_type_btn.clicked.connect(self.device_change_dev_type_btn_pressed)
            self.device_change_connected_btn.clicked.connect(self.device_change_connected_btn_pressed)
            self.device_add_connected_btn.clicked.connect(self.device_add_connected_btn_pressed)
            self.device_delete_connected_btn.clicked.connect(self.device_delete_connected_btn_pressed)
            self.device_connected_list.itemSelectionChanged.connect(self.device_connected_list_selected)
            self.device_dev_types = ''
            self.device_dev_types_parsed = {}
            self.device_dev = []
            self.device_dev_parsed = {}
            self.device_dev_selected = db_model.DeviceBase
            self.device_connected = ''
            self.device_connected_parsed = {}
            self.device_change_mode = False
            self.device_connected_selected = db_model.DeviceBase
            #  worker_page
            self.worker_btn.clicked.connect(self.worker_page_show)
            self.worker_work = ''
            self.worker_work_parsed = {}
            self.worker_work_list.itemSelectionChanged.connect(self.worker_work_list_selected)
            self.worker_work_selected = db_model.WorkerBase
            self.worker_criteria = ''
            self.worker_criteria_parsed = {}
            self.worker_criteria_selected = db_model.InsiderCriteriaBase
            self.worker_delete_btn.clicked.connect(self.worker_delete_btn_pressed)
            self.worker_add_btn.clicked.connect(self.worker_add_btn_pressed)
            self.worker_change_btn.clicked.connect(self.worker_change_btn_pressed)
            self.worker_criteria_list.itemSelectionChanged.connect(self.worker_criteria_list_selected)
            self.worker_criteria_parsed_1 = {}
            self.worker_criteria_parsed_2 = {}
            self.worker_change_value_btn.clicked.connect(self.worker_change_value_btn_pressed)
            self.worker_result_btn.clicked.connect(self.worker_result_btn_pressed)
            #  vul_page
            self.vulnerability_btn.clicked.connect(self.vulnerability_page_show)
            self.vulnerability_search_btn.clicked.connect(self.vulnerability_search_btn_pressed)
            self.vulnerability_vul_list.itemSelectionChanged.connect(self.vulnerability_vul_list_selected)
            self.vulnerability_vul_selected = db_model.VulnerabilityBase
            self.vulnerability_back_btn.clicked.connect(self.vulnerability_back_btn_pressed)
            self.vulnerability_next_btn.clicked.connect(self.vulnerability_next_btn_pressed)
            self.vulnerability_vul = ''
            self.vulnerability_vul_parsed = {}
            self.vul_count = math.ceil(int(count_vulnerabilities(self.engine)) / 10)
            #  impact_page
            self.impact_btn.clicked.connect(self.impact_page_show)
            self.impact_imp_list.itemSelectionChanged.connect(self.impact_imp_list_selected)
            self.impact_delete_btn.clicked.connect(self.impact_delete_btn_pressed)
            self.impact_add_btn.clicked.connect(self.impact_add_btn_pressed)
            self.impact_imp_selected = db_model.ImpactTypeBase
            self.impact_get_imp = ''
            self.impact_get_imp_parsed = {}
            #  tactic_page
            self.tactic_btn.clicked.connect(self.tactic_page_show)
            self.tactic_tac_list.itemSelectionChanged.connect(self.tactic_tac_list_selected)
            self.tactic_tech_list.itemSelectionChanged.connect(self.tactic_tech_list_selected)
            self.tactic_tac_selected = db_model.TacticBase
            self.tactic_tech_selected = db_model.TechniqueBase
            self.tactic_tac = ''
            self.tactic_tac_parsed = {}
            self.tactic_tech = ''
            self.tactic_tech_parsed = {}
            self.tactic_tac_delete_btn.clicked.connect(self.tactic_tac_delete_btn_pressed)
            self.tactic_tech_delete_btn.clicked.connect(self.tactic_tech_delete_btn_pressed)
            self.tactic_tac_add_btn.clicked.connect(self.tactic_tac_add_btn_pressed)
            self.tactic_tech_add_btn.clicked.connect(self.tactic_tech_add_btn_pressed)
            #  organization_page
            self.organization_btn.clicked.connect(self.organization_page_show)
            self.organization_worker_list.itemSelectionChanged.connect(self.organization_worker_list_selected)
            self.organization_worker_selected = db_model.OrganizationResponsibilityBase
            self.organization_worker = ''
            self.organization_worker_parsed = {}
            self.organization_worker_delete_btn.clicked.connect(self.organization_worker_delete_btn_pressed)
            self.organization_worker_add_btn.clicked.connect(self.organization_worker_add_btn_pressed)
            self.organization_name_change_btn.clicked.connect(self.organization_change_btn_pressed)
            self.organization_obj = db_model.OrganizationBase
            #  intruder_page
            self.intruder_btn.clicked.connect(self.intruder_page_show)
            self.intruder_int_list.itemSelectionChanged.connect(self.intruder_int_list_selected)
            self.intruder_int_selected = db_model.IntruderBase
            self.intruder_int = ''
            self.intruder_int_parsed = {}
            self.intruder_int_delete_btn.clicked.connect(self.intruder_int_delete_btn_pressed)
            self.intruder_int_change_btn.clicked.connect(self.intruder_int_change_btn_pressed)
            self.intruder_int_add_btn.clicked.connect(self.intruder_int_add_btn_pressed)
            self.intruder_int_status_check.clicked.connect(self.intruder_int_status_checked)
            self.intruder_int_add_status_check.clicked.connect(self.intruder_int_add_status_checked)
            self.intruder_place = ''
            self.intruder_place_parsed = {}
            self.intruder_capabilities = ''
            self.intruder_capabilities_parsed = {}
            #  insider_criteria_page
            self.insider_criteria_btn.clicked.connect(self.insider_criteria_page_show)
            self.insider_criteria_list.itemSelectionChanged.connect(self.insider_criteria_list_selected)
            self.insider_criteria_selected = db_model.InsiderCriteriaBase
            self.insider_criteria = ''
            self.insider_criteria_parsed = {}
            self.insider_criteria_delete_btn.clicked.connect(self.insider_criteria_delete_btn_pressed)
            self.insider_criteria_change_btn.clicked.connect(self.insider_criteria_change_btn_pressed)
            self.insider_criteria_add_btn.clicked.connect(self.insider_criteria_add_btn_pressed)
            self.insider_criteria_value_list.itemSelectionChanged.connect(self.insider_criteria_value_list_selected)
            self.insider_criteria_value_selected = db_model.InsiderCriteriaTypeBase
            self.insider_criteria_value = ''
            self.insider_criteria_value_parsed = {}
            self.insider_criteria_type_change_btn.clicked.connect(self.insider_criteria_type_change_btn_pressed)
            self.insider_criteria_type_add_btn.clicked.connect(self.insider_criteria_type_add_btn_pressed)
            self.insider_criteria_value_delete_btn.clicked.connect(self.insider_criteria_value_delete_btn_pressed)
            #
            self.window_load()
        except Exception as e:
            print('AdminWindow')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def threat_page_show(self):
        self.threat_get_ubi = get_all_ubi(self.engine)
        ubi_list = []
        for i in self.threat_get_ubi:
            ubi_list.append(f'УБИ.{beautify_ubi(int(i.id))}')
            self.threat_get_ubi_parsed[f'УБИ.{beautify_ubi(int(i.id))}'] = i
        self.threat_ubi_list.addItems(ubi_list)
        self.enable_all_buttons()
        self.stackedWidget.setCurrentWidget(self.threat_page)
        self.threat_btn.setEnabled(False)
        self.get_all_object_type()

    def negative_page_show(self):
        self.enable_all_buttons()
        self.stackedWidget.setCurrentWidget(self.negative_page)
        self.negative_btn.setEnabled(False)
        self.negative_delete_btn.setEnabled(False)
        self.negative_neg_list_update()

    def object_page_show(self):
        self.enable_all_buttons()
        self.stackedWidget.setCurrentWidget(self.object_page)
        self.object_obj_list.clear()
        self.object_interface_list.clear()
        self.object_obj_list_update()
        self.object_get_all_interfaces()
        self.object_btn.setEnabled(False)

    def interface_page_show(self):
        self.enable_all_buttons()
        self.stackedWidget.setCurrentWidget(self.interface_page)
        self.interface_btn.setEnabled(False)
        self.interface_get_all_realization_ways()
        self.interface_int_list_update()

    def device_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.device_page)
            self.device_btn.setEnabled(False)
            self.device_dev_list_update()
            self.device_set_dev_type()
        except Exception as e:
            print(e)

    def worker_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.worker_page)
            self.worker_btn.setEnabled(False)
            self.worker_work_list_update()
        except Exception as e:
            print(e)

    def tactic_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.tactic_page)
            self.tactic_btn.setEnabled(False)
            self.tactic_tac_list_update()
        except Exception as e:
            print(e)

    def organization_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.organization_page)
            self.organization_btn.setEnabled(False)
            self.organization_worker_list_update()
            self.organization_obj = get_some_by_id(self.engine, db_model.OrganizationBase, 1)
            self.organization_name_le.setText(self.organization_obj.name)
        except Exception as e:
            print(e)

    def vulnerability_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.vulnerability_page)
            self.vulnerability_btn.setEnabled(False)
            self.vulnerability_vul_list_update()
        except Exception as e:
            print(e)

    def insider_criteria_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.insider_criteria_page)
            self.insider_criteria_btn.setEnabled(False)
            self.insider_criteria_list_update()
        except Exception as e:
            print(e)

    def intruder_page_show(self):
        try:
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.intruder_page)
            self.intruder_btn.setEnabled(False)
            self.intruder_int_list_update()
            self.intruder_place = ['Внешний', 'Внутренний']
            self.intruder_place_parsed = {0: 'Внутренний', 1: 'Внешний'}
            self.intruder_capabilities = ['H1. Нарушитель, обладающий базовыми возможностями',
                                          'Н2. Нарушитель, обладающий базовыми повышенными возможностями',
                                          'H3. Нарушитель, обладающий средними возможностями',
                                          'H4. Нарушитель, обладающий высокими возможностями']
            self.intruder_capabilities_parsed = {0: 'H1. Нарушитель, обладающий базовыми возможностями',
                                                 1: 'Н2. Нарушитель, обладающий базовыми повышенными возможностями',
                                                 2: 'H3. Нарушитель, обладающий средними возможностями',
                                                 3: 'H4. Нарушитель, обладающий высокими возможностями'}
            self.intruder_int_add_place_cb.clear()
            self.intruder_int_add_capabilities_cb.clear()
            self.intruder_int_add_place_cb.addItems(self.intruder_place)
            self.intruder_int_add_capabilities_cb.addItems(self.intruder_capabilities)
        except Exception as e:
            print(e)

    def intruder_int_list_update(self):
        try:
            self.intruder_int_list.clear()
            self.intruder_int_name_te.clear()
            self.intruder_int_place_cb.clear()
            self.intruder_int_capabilities_cb.clear()
            self.intruder_int_aim_te.clear()
            self.intruder_int_status_check.setChecked(False)
            self.intruder_int_status_reason_le.clear()
            self.intruder_get_int()
            self.intruder_int_list.addItems(self.intruder_int)
        except Exception as e:
            print(e)

    def intruder_get_int(self):
        try:
            self.intruder_int_parsed.clear()
            self.intruder_int = get_all_some(self.engine, db_model.IntruderBase)
            intruder_int = []
            for i in self.intruder_int:
                intruder_int.append(f'{i.name}')
                self.intruder_int_parsed[f'{i.name}'] = i
            self.intruder_int = intruder_int
        except Exception as e:
            print(e)

    def intruder_int_list_selected(self):
        try:
            self.intruder_int_place_cb.clear()
            self.intruder_int_capabilities_cb.clear()
            a = self.intruder_int_list.selectedItems()[0].text()
            self.intruder_int_delete_btn.setEnabled(True)
            self.intruder_int_selected = self.intruder_int_parsed[a]
            self.intruder_int_name_te.setPlainText(self.intruder_int_selected.name)
            self.intruder_int_aim_te.setPlainText(self.intruder_int_selected.aims)
            if self.intruder_int_selected.place == 1:
                self.intruder_int_place_cb.addItem('Внешний')
                self.intruder_int_place_cb.addItem('Внутренний')
            else:
                self.intruder_int_place_cb.addItem('Внутренний')
                self.intruder_int_place_cb.addItem('Внешний')
            if self.intruder_int_selected.capabilities == 0:
                self.intruder_int_capabilities_cb.addItem('H1. Нарушитель, обладающий базовыми возможностями')
                self.intruder_int_capabilities_cb.addItem(
                    'Н2. Нарушитель, обладающий базовыми повышенными возможностями')
                self.intruder_int_capabilities_cb.addItem('H3. Нарушитель, обладающий средними возможностями')
                self.intruder_int_capabilities_cb.addItem('H4. Нарушитель, обладающий высокими возможностями')
            elif self.intruder_int_selected.capabilities == 1:
                self.intruder_int_capabilities_cb.addItem(
                    'Н2. Нарушитель, обладающий базовыми повышенными возможностями')
                self.intruder_int_capabilities_cb.addItem('H1. Нарушитель, обладающий базовыми возможностями')
                self.intruder_int_capabilities_cb.addItem('H3. Нарушитель, обладающий средними возможностями')
                self.intruder_int_capabilities_cb.addItem('H4. Нарушитель, обладающий высокими возможностями')
            elif self.intruder_int_selected.capabilities == 2:
                self.intruder_int_capabilities_cb.addItem('H3. Нарушитель, обладающий средними возможностями')
                self.intruder_int_capabilities_cb.addItem('H1. Нарушитель, обладающий базовыми возможностями')
                self.intruder_int_capabilities_cb.addItem(
                    'Н2. Нарушитель, обладающий базовыми повышенными возможностями')
                self.intruder_int_capabilities_cb.addItem('H4. Нарушитель, обладающий высокими возможностями')
            else:
                self.intruder_int_capabilities_cb.addItem('H4. Нарушитель, обладающий высокими возможностями')
                self.intruder_int_capabilities_cb.addItem('H1. Нарушитель, обладающий базовыми возможностями')
                self.intruder_int_capabilities_cb.addItem(
                    'Н2. Нарушитель, обладающий базовыми повышенными возможностями')
                self.intruder_int_capabilities_cb.addItem('H3. Нарушитель, обладающий средними возможностями')
            if self.intruder_int_selected.status == 0:
                self.intruder_int_status_check.setCheckState(False)
                self.intruder_int_status_reason_le.setEnabled(True)
            else:
                self.intruder_int_status_check.setCheckState(True)
                self.intruder_int_status_reason_le.setEnabled(False)
            self.intruder_int_status_reason_le.setText(self.intruder_int_selected.status_reason)
        except Exception as e:
            print(e)

    def intruder_int_delete_btn_pressed(self):
        delete_some_by_parameter(self.engine, obj=db_model.DeviceTypeIntruderBase,
                                 parameter=db_model.DeviceTypeIntruderBase.intruder_id,
                                 number=self.intruder_int_selected.id)
        delete_some_by_id(self.engine, db_model.IntruderBase, self.intruder_int_selected.id)
        self.intruder_int_list_update()

    def intruder_int_add_btn_pressed(self):
        name = self.intruder_int_add_name_te.toPlainText()
        intruder_place_parsed = {'Внутренний': 0, 'Внешний': 1}
        intruder_capabilities_parsed = {'H1. Нарушитель, обладающий базовыми возможностями': 0,
                                        'Н2. Нарушитель, обладающий базовыми повышенными возможностями': 1,
                                        'H3. Нарушитель, обладающий средними возможностями': 2,
                                        'H4. Нарушитель, обладающий высокими возможностями': 3}
        place = intruder_place_parsed[self.intruder_int_add_place_cb.currentText()]
        capabilities = intruder_capabilities_parsed[self.intruder_int_add_capabilities_cb.currentText()]
        aims = self.intruder_int_add_aim_te.toPlainText()
        if self.intruder_int_add_status_check.isChecked():
            status = 1
            status_reason = ''
        else:
            status = 0
            status_reason = self.intruder_int_add_status_reason_le.text()
        if name != '' and name is not None and aims != '' and aims is not None:
            create_some(
                db_model.IntruderBase(name=name, place=place, capabilities=capabilities, aims=aims, status=status,
                                      status_reason=status_reason), self.engine)
            self.intruder_int_list_update()

    def intruder_int_change_btn_pressed(self):
        try:
            name = self.intruder_int_name_te.toPlainText()
            intruder_place_parsed = {'Внутренний': 0, 'Внешний': 1}
            intruder_capabilities_parsed = {'H1. Нарушитель, обладающий базовыми возможностями': 0,
                                            'Н2. Нарушитель, обладающий базовыми повышенными возможностями': 1,
                                            'H3. Нарушитель, обладающий средними возможностями': 2,
                                            'H4. Нарушитель, обладающий высокими возможностями': 3}
            place = intruder_place_parsed[self.intruder_int_add_place_cb.currentText()]
            capabilities = intruder_capabilities_parsed[self.intruder_int_capabilities_cb.currentText()]
            aims = self.intruder_int_aim_te.toPlainText()
            if self.intruder_int_status_check.isChecked():
                status = 1
                status_reason = ''
            else:
                status = 0
                status_reason = self.intruder_int_status_reason_le.text()
            if name != '' and name is not None and aims != '' and aims is not None:
                obj = self.intruder_int_selected
                obj.name = name
                obj.place = place
                obj.capabilities = capabilities
                obj.status = status
                obj.status_reason = status_reason
                update_some_by_id(self.engine, obj)
                self.intruder_int_list_update()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def intruder_int_status_checked(self):
        if self.intruder_int_status_check.isChecked():
            self.intruder_int_status_reason_le.setEnabled(False)
        else:
            self.intruder_int_status_reason_le.setEnabled(True)

    def intruder_int_add_status_checked(self):
        if self.intruder_int_add_status_check.isChecked():
            self.intruder_int_add_status_reason_le.setEnabled(False)
        else:
            self.intruder_int_add_status_reason_le.setEnabled(True)

    def insider_criteria_list_update(self):
        try:
            self.insider_criteria_list.clear()
            self.insider_criteria_name_le.clear()
            self.insider_criteria_coef_le.clear()
            self.insider_criteria_type_name_le.clear()
            self.insider_criteria_type_value_le.clear()
            self.insider_get_criteria()
            self.insider_criteria_list.addItems(self.insider_criteria)
        except Exception as e:
            print(e)

    def insider_get_criteria(self):
        try:
            self.insider_criteria_parsed.clear()
            self.insider_criteria = get_all_some(self.engine, db_model.InsiderCriteriaBase)
            insider_criteria = []
            for i in self.insider_criteria:
                insider_criteria.append(f'{i.name}')
                self.insider_criteria_parsed[f'{i.name}'] = i
            self.insider_criteria = insider_criteria
        except Exception as e:
            print(e)

    def insider_criteria_list_selected(self):
        try:
            a = self.insider_criteria_list.selectedItems()[0].text()
            self.insider_criteria_delete_btn.setEnabled(True)
            self.insider_criteria_selected = self.insider_criteria_parsed[a]
            self.insider_criteria_name_le.setText(self.insider_criteria_selected.name)
            self.insider_criteria_coef_le.setText(str(self.insider_criteria_selected.coefficient))
            self.insider_get_criteria_type()
            self.insider_criteria_value_list.clear()
            self.insider_criteria_value_list.addItems(self.insider_criteria_value)
        except Exception as e:
            print(e)

    def insider_get_criteria_type(self):
        try:
            self.insider_criteria_value_parsed.clear()
            self.insider_criteria_value = get_insider_criteria_type_by_ins_id(self.engine,
                                                                              self.insider_criteria_selected.id)
            insider_criteria_value = []
            for i in self.insider_criteria_value:
                insider_criteria_value.append(f'{i.name}')
                self.insider_criteria_value_parsed[f'{i.name}'] = i
            self.insider_criteria_value = insider_criteria_value
        except Exception as e:
            print(e)

    def insider_criteria_value_list_selected(self):
        try:
            a = self.insider_criteria_value_list.selectedItems()[0].text()
            self.insider_criteria_value_delete_btn.setEnabled(True)
            self.insider_criteria_value_selected = self.insider_criteria_value_parsed[a]
            self.insider_criteria_type_name_le.setText(self.insider_criteria_value_selected.name)
            self.insider_criteria_type_value_le.setText(str(self.insider_criteria_value_selected.value))
        except Exception as e:
            print(e)

    def insider_criteria_value_delete_btn_pressed(self):
        try:
            work_insider = get_worker_insider_by_type_id(self.engine, self.insider_criteria_selected.id,
                                                         self.insider_criteria_value_selected.id)
            for obj in work_insider:
                obj.value = 1
                update_some_by_id(self.engine, obj)
            delete_insider_criteria_type(self.engine, self.insider_criteria_selected.id,
                                         self.insider_criteria_value_selected.id)
            self.insider_criteria_list_selected()
        except Exception as e:
            print(e)

    def insider_criteria_type_change_btn_pressed(self):
        try:
            name = self.insider_criteria_type_name_le.text()
            value = self.insider_criteria_type_value_le.text()
            obj = self.insider_criteria_value_selected
            if name != '' and 0 < float(value) < 1:
                obj.name = name
                obj.value = float(value)
                update_some_by_id(self.engine, obj)
                self.insider_criteria_list_selected()
        except Exception as e:
            print(e)

    def insider_criteria_type_add_btn_pressed(self):
        try:
            all_type = get_all_some(self.engine, db_model.InsiderCriteriaTypeBase)
            needed = []
            for o in all_type:
                if o.insider_criteria_id == self.insider_criteria_selected.id:
                    needed.append(o)
            maximum = 0
            for i in needed:
                if i.id > maximum:
                    maximum = i.id
            value = float(self.insider_criteria_type_add_value_le.text())
            name = self.insider_criteria_type_add_name_le.text()
            if name != '' and 0 < float(value) < 1:
                create_some(
                    db_model.InsiderCriteriaTypeBase(name=name, insider_criteria_id=self.insider_criteria_selected.id, id=maximum + 1, value=value),
                    self.engine)
                self.insider_criteria_list_selected()
        except Exception as e:
            print(e)

    def insider_criteria_delete_btn_pressed(self):
        try:
            delete_worker_insider_criteria_by_id(self.engine, self.insider_criteria_selected.id)
            delete_some_by_id(self.engine, db_model.InsiderCriteriaBase, self.insider_criteria_selected.id)
            self.insider_criteria_list_update()
        except Exception as e:
            print(e)

    def insider_criteria_add_btn_pressed(self):
        try:
            name = self.insider_criteria_add_name_le.text()
            coefficient = self.insider_criteria_add_coef_le.text()
            create_some(
                db_model.InsiderCriteriaBase(name=name, coefficient=int(coefficient)),
                self.engine)
            workers = get_all_some(self.engine, db_model.WorkerBase)
            insider_criteria = get_all_some(self.engine, db_model.InsiderCriteriaBase)
            for i in workers:
                create_some(
                    db_model.WorkerInsiderCriteriaBase(worker_id=i.id, insider_criteria_id=insider_criteria[-1].id),
                    self.engine)
            self.insider_criteria_list_update()
            self.insider_criteria_add_name_le.clear()
            self.insider_criteria_add_coef_le.clear()
        except Exception as e:
            print(e)

    def insider_criteria_change_btn_pressed(self):
        try:
            name = self.insider_criteria_name_le.text()
            coefficient = self.insider_criteria_coef_le.text()
            if name != '' and name is not None and name != '' and coefficient is not None and coefficient != '':
                obj = self.insider_criteria_selected
                obj.name = name
                obj.coefficient = coefficient
                update_some_by_id(self.engine, obj)
                self.insider_criteria_list_update()
        except Exception as e:
            print(e)

    def vulnerability_vul_list_update(self):
        try:
            self.vulnerability_vul_list.clear()
            self.vulnerability_type_le.clear()
            self.vulnerability_description_te.clear()
            self.vulnerability_software_list.clear()
            self.vulnerability_get_vul()
            self.vulnerability_vul_list.addItems(self.vulnerability_vul)
        except Exception as e:
            print(e)

    def vulnerability_get_vul(self):
        try:
            self.vulnerability_vul_parsed.clear()
            self.vulnerability_vul = get_vulnerabilities(self.engine, 10, int(self.vulnerability_count_page_lbl.text()))
            vulnerability_vul = []
            for i in self.vulnerability_vul:
                vulnerability_vul.append(f'{i.code} {i.name}')
                self.vulnerability_vul_parsed[f'{i.code} {i.name}'] = i
            self.vulnerability_vul = vulnerability_vul
        except Exception as e:
            print(e)

    def vulnerability_vul_list_selected(self):
        try:
            a = self.vulnerability_vul_list.selectedItems()[0].text()
            self.vulnerability_vul_selected = self.vulnerability_vul_parsed[a]
            types = get_vulnerability_type_by_vul_id(self.engine, self.vulnerability_vul_selected.id)
            temp = ''
            for i in types:
                temp += i.name + ", "
            self.vulnerability_type_le.setText(temp[:-2])
            self.vulnerability_description_te.setPlainText(self.vulnerability_vul_selected.description)
            software = get_vulnerability_software_by_vul_id(self.engine, self.vulnerability_vul_selected.id)
            temp = []
            for i in software:
                temp.append(i.name.strip(' '))
            temp = list(set(temp))
            self.vulnerability_software_list.clear()
            for i in temp:
                if i != '' and i != ' ' and i != 'R':
                    print(i)
                    self.vulnerability_software_list.addItem(i)
        except Exception as e:
            print(e)

    def vulnerability_back_btn_pressed(self):
        try:
            page = int(self.vulnerability_count_page_lbl.text()) - 1
            if page >= 1:
                self.vulnerability_count_page_lbl.setText(str(page))
                self.vulnerability_vul_list_update()
        except Exception as e:
            print(e)

    def vulnerability_next_btn_pressed(self):
        try:
            page = int(self.vulnerability_count_page_lbl.text()) + 1
            if page <= self.vul_count:
                self.vulnerability_count_page_lbl.setText(str(page))
                self.vulnerability_vul_list_update()
        except Exception as e:
            print(e)

    def vulnerability_search_btn_pressed(self):
        if self.vulnerability_search_le.text() == '':
            self.vulnerability_next_btn.setEnabled(True)
            self.vulnerability_back_btn.setEnabled(True)
            self.vulnerability_vul_list_update()
        else:
            self.vulnerability_next_btn.setEnabled(False)
            self.vulnerability_back_btn.setEnabled(False)
            self.vulnerability_vul_list.clear()
            self.vulnerability_vul_parsed.clear()
            self.vulnerability_vul = vulnerability_search(self.engine, self.vulnerability_search_le.text())
            print(self.vulnerability_vul)
            vulnerability_vul = []
            for i in self.vulnerability_vul:
                vulnerability_vul.append(f'{i.code} {i.name}')
                self.vulnerability_vul_parsed[f'{i.code} {i.name}'] = i
            self.vulnerability_vul = vulnerability_vul
            self.vulnerability_vul_list.addItems(self.vulnerability_vul)

    def organization_worker_list_update(self):
        try:
            self.organization_worker_list.clear()
            self.organization_worker_name_le.clear()
            self.organization_worker_surname_le.clear()
            self.organization_worker_patronymic_le.clear()
            self.organization_worker_role_le.clear()
            self.organization_get_worker()
            self.organization_worker_list.addItems(self.organization_worker)
            self.organization_worker_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def organization_get_worker(self):
        try:
            self.organization_worker_parsed.clear()
            self.organization_worker = get_all_some(self.engine, db_model.OrganizationResponsibilityBase)
            organization_worker = []
            for i in self.organization_worker:
                organization_worker.append(f'{i.id} | {i.name} {i.surname} {i.patronymic}')
                self.organization_worker_parsed[f'{i.id} | {i.name} {i.surname} {i.patronymic}'] = i
            self.organization_worker = organization_worker
        except Exception as e:
            print(e)

    def organization_worker_list_selected(self):
        try:
            a = self.organization_worker_list.selectedItems()[0].text()
            self.organization_worker_delete_btn.setEnabled(True)
            self.organization_worker_selected = self.organization_worker_parsed[a]
            self.organization_worker_name_le.setText(self.organization_worker_selected.name)
            self.organization_worker_surname_le.setText(self.organization_worker_selected.surname)
            self.organization_worker_patronymic_le.setText(self.organization_worker_selected.patronymic)
            self.organization_worker_role_le.setText(self.organization_worker_selected.role)
        except Exception as e:
            print(e)

    def organization_worker_delete_btn_pressed(self):
        delete_some_by_id(self.engine, db_model.OrganizationResponsibilityBase, self.organization_worker_selected.id)
        self.organization_worker_list_update()

    def organization_worker_add_btn_pressed(self):
        name = self.organization_worker_add_name_le.text()
        surname = self.organization_worker_add_surname_le.text()
        patronymic = self.organization_worker_add_patronymic_le.text()
        role = self.organization_worker_add_role_le.text()
        create_some(
            db_model.OrganizationResponsibilityBase(name=name, surname=surname, patronymic=patronymic, role=role),
            self.engine)
        self.organization_worker_list_update()

    def organization_change_btn_pressed(self):
        org_name = self.organization_name_le.text()
        if org_name != '' and org_name is not None:
            obj = self.organization_obj
            obj.name = org_name
            update_some_by_id(self.engine, obj)

    def tactic_tac_list_update(self):
        try:
            self.tactic_tac_list.clear()
            self.tactic_tech_list.clear()
            self.tactic_get_tactic()
            self.tactic_tac_list.addItems(self.tactic_tac)
            self.tactic_tac_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def tactic_get_tactic(self):
        try:
            self.tactic_tac_parsed.clear()
            self.tactic_tac = get_all_some(self.engine, db_model.TacticBase)
            tactic_tac = []
            for i in self.tactic_tac:
                tactic_tac.append(f'T{i.id} {i.name}')
                self.tactic_tac_parsed[f'T{i.id} {i.name}'] = i
            self.tactic_tac = tactic_tac
        except Exception as e:
            print(e)

    def tactic_tac_list_selected(self):
        try:
            self.tactic_tac_delete_btn.setEnabled(True)
            self.tactic_tech_list.clear()
            self.tactic_tac_selected = self.tactic_tac_parsed[
                self.tactic_tac_list.selectedItems()[0].text()]
            self.tactic_get_technique()
        except Exception as e:
            print(e)

    def tactic_get_technique(self):
        self.tactic_tech_parsed.clear()
        self.tactic_tech = get_technique_by_tac_id(self.engine, self.tactic_tac_selected.id)
        tactic_tech = []
        for i in self.tactic_tech:
            tactic_tech.append(f'T{i.tactic_id}.{i.technique_id} {i.name}')
            self.tactic_tech_parsed[f'T{i.tactic_id}.{i.technique_id} {i.name}'] = i
        self.tactic_tech = tactic_tech
        self.tactic_tech_list.addItems(self.tactic_tech)

    def tactic_tac_delete_btn_pressed(self):
        try:
            delete_some_by_id(self.engine, db_model.TacticBase, self.tactic_tac_selected.id)
            self.tactic_tac_list_update()
        except Exception as e:
            print(e)

    def tactic_tech_delete_btn_pressed(self):
        try:
            delete_some_by_id(self.engine, db_model.TechniqueBase, self.tactic_tech_selected.id)
            self.tactic_tac_list_selected()
        except Exception as e:
            print(e)

    def tactic_tac_add_btn_pressed(self):
        try:
            a = 0
            for i in self.tactic_tac_parsed.values():
                if a < i.id:
                    a = i.id
            create_some(db_model.TacticBase(id=a + 1, name=self.tactic_tac_add_te.toPlainText()), self.engine)
            self.tactic_tac_list_update()
        except Exception as e:
            print(e)

    def tactic_tech_add_btn_pressed(self):
        try:
            a = 0
            for i in self.tactic_tech_parsed.values():
                if a < i.technique_id:
                    a = i.technique_id
            create_some(db_model.TechniqueBase(name=self.tactic_tech_add_te.toPlainText(),
                                               tactic_id=self.tactic_tac_selected.id, technique_id=a + 1), self.engine)
            self.tactic_tac_list_selected()
        except Exception as e:
            print(e)

    def tactic_tech_list_selected(self):
        try:
            self.tactic_tech_delete_btn.setEnabled(True)
            self.tactic_tech_selected = self.tactic_tech_parsed[
                self.tactic_tech_list.selectedItems()[0].text()]
        except Exception as e:
            print(e)

    def worker_work_list_update(self):
        try:
            self.worker_name_le.clear()
            self.worker_surname_le.clear()
            self.worker_patronymic_le.clear()
            self.worker_description_te.clear()
            self.worker_result_le.clear()
            self.worker_work_list.clear()
            self.worker_criteria_list.clear()
            self.worker_get_all_worker()
            self.worker_work_list.addItems(self.worker_work)
            self.worker_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def worker_get_all_worker(self):
        try:
            self.worker_work = get_all_some(self.engine, db_model.WorkerBase)
            worker_work = []
            for i in self.worker_work:
                worker_work.append(f'{i.id} | {i.name} {i.surname} {i.patronymic}')
                self.worker_work_parsed[f'{i.id} | {i.name} {i.surname} {i.patronymic}'] = i
            self.worker_work = worker_work
        except Exception as e:
            print(e)

    def worker_work_list_selected(self):
        try:
            self.worker_delete_btn.setEnabled(True)
            self.worker_name_le.clear()
            self.worker_surname_le.clear()
            self.worker_patronymic_le.clear()
            self.worker_description_te.clear()
            self.worker_criteria_list.clear()
            self.worker_work_selected = self.worker_work_parsed[
                self.worker_work_list.selectedItems()[0].text()]
            self.worker_name_le.setText(self.worker_work_selected.name)
            self.worker_surname_le.setText(self.worker_work_selected.surname)
            self.worker_patronymic_le.setText(self.worker_work_selected.patronymic)
            self.worker_description_te.setPlainText(self.worker_work_selected.description)
            self.worker_result_le.setText(str(self.worker_work_selected.insider_result))
            self.worker_get_criteria()
        except Exception as e:
            print(e)

    def worker_get_criteria(self):
        self.worker_criteria_parsed.clear()
        self.worker_criteria = get_worker_criteria(self.engine, self.worker_work_selected.id)
        worker_criteria = []
        for i in self.worker_criteria:
            worker_criteria.append(f'{i[0]}')
            self.worker_criteria_parsed[f'{i[0]}'] = i
        self.worker_criteria = worker_criteria
        self.worker_criteria_list.addItems(self.worker_criteria)

    def worker_delete_btn_pressed(self):
        delete_worker_criteria_by_id(self.engine, self.worker_work_selected.id)
        delete_some_by_id(self.engine, db_model.WorkerBase, self.worker_work_selected.id)
        self.worker_work_list_update()

    def worker_add_btn_pressed(self):
        name = self.worker_add_name_le.text()
        surname = self.worker_add_surname_le.text()
        patronymic = self.worker_add_patronymic_le.text()
        description = self.worker_add_description_te.toPlainText()
        if name != '' and name is not None:
            if surname != '' and surname is not None:
                if description is None:
                    description = ''
                if patronymic is None:
                    patronymic = ''
                create_some(
                    db_model.WorkerBase(name=name, surname=surname, patronymic=patronymic, description=description),
                    self.engine)
                self.worker_work_list_update()
                worker = get_all_some(self.engine, db_model.WorkerBase)
                worker = worker[-1]
                criteria = get_all_some(self.engine, db_model.InsiderCriteriaBase)
                for i in criteria:
                    create_some(db_model.WorkerInsiderCriteriaBase(worker_id=worker.id, insider_criteria_id=i.id),
                                self.engine)

    def worker_change_btn_pressed(self):
        name = self.worker_name_le.text()
        surname = self.worker_surname_le.text()
        patronymic = self.worker_patronymic_le.text()
        description = self.worker_description_te.toPlainText()
        if name != '' and name is not None:
            if surname != '' and surname is not None:
                if description is None:
                    description = ''
                if patronymic is None:
                    patronymic = ''
                obj = self.worker_work_selected
                obj.name = name
                obj.surname = surname
                obj.patronymic = patronymic
                obj.description = description
                update_some_by_id(self.engine, obj)
                self.worker_work_list_update()

    def worker_criteria_list_selected(self):
        try:
            self.worker_criteria_parsed_1.clear()
            self.worker_criteria_parsed_2.clear()
            self.worker_criteria_selected = self.worker_criteria_parsed[
                self.worker_criteria_list.selectedItems()[0].text()]
            print(self.worker_criteria_parsed)
            print(self.worker_work_selected.id)
            print(self.worker_criteria_selected.id)
            criteria_type = get_criteria_type(self.engine, self.worker_work_selected.id,
                                              self.worker_criteria_selected[4])
            values = []
            for i in criteria_type:
                self.worker_criteria_parsed_2[i[1]] = i
                values.append(i[1])
            self.worker_value_cb.clear()
            self.worker_value_cb.addItems(values)
            self.worker_value_le.setText(self.worker_criteria_selected[-2])
            self.worker_coef_le.setText(str(self.worker_criteria_selected[1]))
        except Exception as e:
            print(e)

    def worker_change_value_btn_pressed(self):
        try:
            value = self.worker_criteria_parsed_2[self.worker_value_cb.currentText()][0]
            obj = db_model.WorkerInsiderCriteriaBase(worker_id=self.worker_criteria_selected[3],
                                                     insider_criteria_id=self.worker_criteria_selected[4], value=value)
            update_some_by_id(self.engine, obj)
            self.worker_work_list_selected()
            self.worker_value_le.clear()
            self.worker_coef_le.clear()
        except Exception as e:
            print(e)

    def worker_result_btn_pressed(self):
        try:
            result = 0.0
            parts = 0.0
            for i in self.worker_criteria_parsed.values():
                parts += i[1]
            for i in self.worker_criteria_parsed.items():
                result = result + ((i[1][1] / parts) * float(i[1][-1]))
            result = round(result, 3)
            self.worker_result_le.setText(str(result))
            obj = self.worker_work_selected
            obj.insider_result = result
            update_some_by_id(self.engine, obj)
        except Exception as e:
            print(e)

    def device_dev_list_update(self):
        try:
            self.device_ip_te.clear()
            self.device_description_te.clear()
            self.device_dev_list.clear()
            self.device_connected_list.clear()
            self.device_dev_type_te.clear()
            self.device_get_all_device()
            self.device_dev_list.addItems(self.device_dev)
            self.device_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def device_get_all_device(self):
        try:
            self.device_dev = get_all_some(self.engine, db_model.DeviceBase)
            device_dev = []
            for i in self.device_dev:
                ips = get_ip(self.engine, i.id)
                string_ip = ''
                for ip in ips:
                    string_ip += ip.ip_address + ' '
                device_dev.append(f'{i.id} | {string_ip}')
                self.device_dev_parsed[f'{i.id} | {string_ip}'] = i
            self.device_dev = device_dev
        except Exception as e:
            print(e)

    def device_set_dev_type(self):
        try:
            self.device_dev_types = get_all_some(self.engine, db_model.DeviceTypeBase)
            device_dev_types = []
            for i in self.device_dev_types:
                device_dev_types.append(f'{i.name}')
                self.device_dev_types_parsed[f'{i.name}'] = i
            self.realization_get_real = device_dev_types
            self.device_dev_type_cb.addItems(self.realization_get_real)
        except Exception as e:
            print(e)

    def device_dev_list_selected(self):
        try:
            self.device_delete_btn.setEnabled(True)
            self.device_description_te.clear()
            self.device_ip_te.clear()
            self.device_dev_type_te.clear()
            self.device_connected_list.clear()
            self.device_dev_selected = self.device_dev_parsed[
                self.device_dev_list.selectedItems()[0].text()]
            self.device_description_te.setPlainText(self.device_dev_selected.description)
            ips = get_ip(self.engine, self.device_dev_selected.id)
            string_ip = ''
            for ip in ips:
                string_ip += ip.ip_address + ' '
            self.device_ip_te.setPlainText(string_ip)
            if self.device_dev_selected.type_id is not None:
                dev_type = get_some_by_id(self.engine, db_model.DeviceTypeBase, self.device_dev_selected.type_id)
                self.device_dev_type_te.setPlainText(dev_type.name)
            self.device_get_connected()
        except Exception as e:
            print(e)

    def device_get_connected(self):
        self.device_connected_list.clear()
        self.device_connected = get_connected_devices_by_id(self.engine, self.device_dev_selected.id)
        device_connected = []
        for i in self.device_connected:
            ips = get_ip(self.engine, i.id)
            string_ip = ''
            for ip in ips:
                string_ip += ip.ip_address + ' '
            device_connected.append(f'{i.id} | {string_ip}')
            self.device_connected_parsed[f'{i.id} | {string_ip}'] = i
            print(i)
        self.device_connected = device_connected
        self.device_connected_list.addItems(self.device_connected)

    def device_add_btn_pressed(self):
        try:
            ip = self.device_add_ip_le.text()
            description = self.device_add_description_te.toPlainText()
            if ip != '' and ip is not None:
                if description is None:
                    description = ''
                create_some(db_model.DeviceBase(ip_address=ip, description=description), self.engine)
                self.device_dev_list_update()
                self.device_add_ip_le.clear()
                self.device_add_description_te.clear()
        except Exception as e:
            print(e)

    def device_delete_btn_pressed(self):
        try:
            delete_some_by_id(self.engine, db_model.DeviceBase, self.device_dev_selected.id)
            self.device_dev_list_update()
        except Exception as e:
            print(e)

    def device_change_dev_type_btn_pressed(self):
        try:
            obj = self.device_dev_selected
            obj.type_id = self.device_dev_types_parsed[self.device_dev_type_cb.currentText()].id
            update_some_by_id(self.engine, obj)
            self.device_dev_list_selected()
        except Exception as e:
            print(e)

    def device_change_connected_btn_pressed(self):
        try:
            if self.device_change_mode:
                self.device_change_mode = False
                self.device_get_connected()
            else:
                self.device_change_mode = True
                self.device_connected_list.clear()
                devices_without_current = copy.deepcopy(self.device_dev)
                devices_without_current.remove(self.device_dev_selected.ip_address)
                self.device_connected_list.addItems(devices_without_current)
            self.device_add_connected_btn.setEnabled(False)
            self.device_delete_connected_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def device_connected_list_selected(self):
        try:
            if self.device_change_mode:
                self.device_add_connected_btn.setEnabled(True)
                self.device_connected_selected = self.device_dev_parsed[
                    self.device_connected_list.selectedItems()[0].text()]
            else:
                self.device_delete_connected_btn.setEnabled(True)
                self.device_connected_selected = self.device_connected_parsed[
                    self.device_connected_list.selectedItems()[0].text()]
        except Exception as e:
            print(e)

    def device_add_connected_btn_pressed(self):
        try:
            print(self.device_dev_selected)
            print(self.device_connected_selected)
            first_id = self.device_dev_selected.id
            second_id = self.device_connected_selected.id
            create_some(
                db_model.DeviceConnectionBase(first_device_id=first_id, second_device_id=second_id),
                self.engine)
            self.device_change_connected_btn_pressed()
        except Exception as e:
            print(e)

    def device_delete_connected_btn_pressed(self):
        try:
            first_id = self.device_dev_selected.id
            second_id = self.device_connected_selected.id
            delete_device_connection(engine=self.engine, first_id=first_id, second_id=second_id)
            self.device_get_connected()
        except Exception as e:
            print(e)

    def impact_page_show(self):
        try:
            self.impact_name_te.clear()
            self.enable_all_buttons()
            self.stackedWidget.setCurrentWidget(self.impact_page)
            self.impact_btn.setEnabled(False)
            self.impact_imp_list_update()
        except Exception as e:
            print(e)

    def impact_imp_list_update(self):
        try:
            self.impact_name_te.clear()
            self.impact_imp_list.clear()
            self.get_all_impact()
            self.impact_imp_list.addItems(self.impact_get_imp)
            self.impact_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def impact_add_btn_pressed(self):
        self.impact_name_te.clear()
        name = self.impact_add_le.text()
        if name != '' and name is not None:
            create_some(db_model.ImpactTypeBase(name=name), self.engine)
            self.impact_imp_list_update()
            self.impact_add_le.clear()

    def impact_delete_btn_pressed(self):
        try:
            delete_some_by_id(self.engine, db_model.ImpactTypeBase, self.impact_imp_selected.id)
            self.impact_imp_list_update()
            self.impact_name_te.clear()
        except Exception as e:
            print(e)

    def impact_imp_list_selected(self):
        try:
            self.impact_delete_btn.setEnabled(True)
            self.impact_name_te.clear()
            self.impact_imp_selected = self.impact_get_imp_parsed[
                self.impact_imp_list.selectedItems()[0].text()]
            self.impact_name_te.setPlainText(self.impact_imp_selected.name)
        except Exception as e:
            print(e)

    def get_all_impact(self):
        try:
            self.impact_get_imp_parsed.clear()
            self.impact_get_imp = get_all_some(self.engine, db_model.ImpactTypeBase)
            impact_get_imp = []
            for i in self.impact_get_imp:
                impact_get_imp.append(f'{i.name}')
                self.impact_get_imp_parsed[f'{i.name}'] = i
            self.impact_get_imp = impact_get_imp
        except Exception as e:
            print(e)

    def realization_page_show(self):
        self.realization_name_te.clear()
        self.realization_description_te.clear()
        self.enable_all_buttons()
        self.stackedWidget.setCurrentWidget(self.realization_page)
        self.realization_btn.setEnabled(False)
        self.realization_real_list_update()

    def realization_real_list_update(self):
        try:
            self.realization_name_te.clear()
            self.realization_description_te.clear()
            self.realization_real_list.clear()
            self.get_all_realization_ways()
            self.realization_real_list.addItems(self.realization_get_real)
            self.realization_delete_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def realization_add_btn_pressed(self):
        self.realization_name_te.clear()
        self.realization_description_te.clear()
        name = self.realization_add_le.text()
        description = self.realization_add_te.toPlainText()
        if name != '' and name is not None:
            if description is None:
                description = ''
            create_some(db_model.RealizationWayBase(name=name, description=description), self.engine)
            self.realization_real_list_update()
            self.realization_add_le.clear()
            self.realization_add_te.clear()

    def realization_delete_btn_pressed(self):
        try:
            delete_some_by_id(self.engine, db_model.RealizationWayBase, self.realization_real_selected.id)
            self.realization_real_list_update()
            self.realization_name_te.clear()
            self.realization_description_te.clear()
        except Exception as e:
            print(e)

    def realization_real_list_selected(self):
        try:
            self.realization_delete_btn.setEnabled(True)
            self.realization_name_te.clear()
            self.realization_description_te.clear()
            self.realization_real_selected = self.realization_get_real_parsed[
                self.realization_real_list.selectedItems()[0].text()]
            self.realization_name_te.setPlainText(self.realization_real_selected.name)
            self.realization_description_te.setPlainText(self.realization_real_selected.description)
        except Exception as e:
            print(e)

    def get_all_realization_ways(self):
        try:
            self.realization_get_real_parsed.clear()
            self.realization_get_real = get_all_realization_ways(self.engine)
            realization_list = []
            for i in self.realization_get_real:
                realization_list.append(f'{i.name}')
                self.realization_get_real_parsed[f'{i.name}'] = i
            self.realization_get_real = realization_list
        except Exception as e:
            print(e)

    def interface_int_list_update(self):
        try:
            self.interface_int_list.clear()
            self.get_all_interfaces()
            self.interface_int_list.addItems(self.interface_get_int)
            self.interface_delete_btn.setEnabled(False)
            self.interface_add_realization_btn.setEnabled(False)
            self.interface_delete_realization_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def get_all_interfaces(self):
        try:
            self.interface_get_int_parsed.clear()
            self.interface_get_int = get_all_interfaces(self.engine)
            interface_list = []
            for i in self.interface_get_int:
                interface_list.append(f'{i.name}')
                self.interface_get_int_parsed[f'{i.name}'] = i
            self.interface_get_int = interface_list
        except Exception as e:
            print(e)

    def interface_int_list_select(self):
        try:
            self.interface_int_list_selected = self.interface_get_int_parsed[
                self.interface_int_list.selectedItems()[0].text()]
            self.interface_delete_btn.setEnabled(True)
            self.interface_get_interface_realization()
        except Exception as e:
            print(e)

    def interface_get_interface_realization(self):
        self.interface_realization_list.clear()
        self.interface_get_realization_parsed.clear()
        self.interface_get_realization = get_realization_by_interface_id(self.engine,
                                                                         self.interface_int_list_selected.id)
        realization_list = []
        for i in self.interface_get_realization:
            realization_list.append(f'{i.name}')
            self.interface_get_realization_parsed[f'{i.name}'] = i
        self.interface_realization_list.addItems(realization_list)
        self.interface_delete_realization_btn.setEnabled(False)

    def interface_get_all_realization_ways(self):
        try:
            self.interface_get_all_realization_parsed.clear()
            self.interface_get_all_realization = get_all_realization_ways(self.engine)
            realization_list = []
            for i in self.interface_get_all_realization:
                realization_list.append(f'{i.name}')
                self.interface_get_all_realization_parsed[f'{i.name}'] = i
            self.interface_get_all_realization = realization_list
        except Exception as e:
            print(e)

    def interface_int_delete_btn_pressed(self):
        try:
            delete_interface_by_id(self.engine, self.interface_int_list_selected.id)
            self.interface_int_list_update()
            self.interface_realization_list.clear()
        except Exception as e:
            print(e)

    def interface_int_add_btn_pressed(self):
        name = self.interface_add_le.text()
        if name != '' and name is not None:
            create_some(db_model.InterfaceBase(name=name), self.engine)
            self.interface_int_list_update()
            self.interface_add_le.clear()

    def interface_change_realization_btn_pressed(self):
        if self.interface_change_mode:
            self.interface_change_mode = False
            self.interface_get_interface_realization()
        else:
            self.interface_change_mode = True
            self.interface_realization_list.clear()
            self.interface_realization_list.addItems(self.interface_get_all_realization)
        self.interface_add_realization_btn.setEnabled(False)
        self.interface_delete_realization_btn.setEnabled(False)

    def interface_realization_list_selected(self):
        try:
            if self.interface_change_mode:
                self.interface_add_realization_btn.setEnabled(True)
                self.interface_realization_selected = self.interface_get_all_realization_parsed[
                    self.interface_realization_list.selectedItems()[0].text()]
            else:
                self.interface_delete_realization_btn.setEnabled(True)
                self.interface_realization_selected = self.interface_get_realization_parsed[
                    self.interface_realization_list.selectedItems()[0].text()]
        except Exception as e:
            print(e)

    def interface_add_realization_btn_pressed(self):
        realization_way_id = self.interface_realization_selected.id
        interface_id = self.interface_int_list_selected.id
        create_some(
            db_model.InterfaceRealizationWayBase(realization_way_id=realization_way_id, interface_id=interface_id),
            self.engine)
        self.interface_change_realization_btn_pressed()

    def interface_delete_realization_btn_pressed(self):
        realization_way_id = self.interface_realization_selected.id
        interface_id = self.interface_int_list_selected.id
        delete_interface_realization_way_by_id(engine=self.engine, realization_way_id=realization_way_id,
                                               interface_id=interface_id)
        self.interface_get_interface_realization()

    def object_obj_list_update(self):
        try:
            self.object_obj_list.clear()
            self.get_all_object_type()
            self.object_obj_list.addItems(self.threat_get_all_object_type)
            self.object_delete_btn.setEnabled(False)
            self.object_add_interface_btn.setEnabled(False)
            self.object_delete_interface_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def object_obj_list_selected(self):
        try:
            self.object_object_list_select_item = self.threat_get_all_object_type_parsed[
                self.object_obj_list.selectedItems()[0].text()]
            self.object_delete_btn.setEnabled(True)
            print(self.threat_get_all_object_type_parsed[
                self.object_obj_list.selectedItems()[0].text()])
            self.object_description_te.setPlainText(self.object_object_list_select_item.description)
            self.object_get_obj_type_interfaces()
        except Exception as e:
            print(e)

    def object_get_obj_type_interfaces(self):
        self.object_interface_list.clear()
        self.object_get_interface_parsed.clear()
        self.object_get_interface = get_interfaces_by_device_type_id(self.engine,
                                                                     self.object_object_list_select_item.id)
        interface_list = []
        for i in self.object_get_interface:
            interface_list.append(f'{i.name}')
            self.object_get_interface_parsed[f'{i.name}'] = i
        self.object_interface_list.addItems(interface_list)
        self.object_delete_interface_btn.setEnabled(False)

    def object_get_all_interfaces(self):
        try:
            self.object_get_all_interface_parsed.clear()
            self.object_get_all_interface = get_all_interfaces(self.engine)
            interface_list = []
            for i in self.object_get_all_interface:
                interface_list.append(f'{i.name}')
                self.object_get_all_interface_parsed[f'{i.name}'] = i
            self.object_get_all_interface = interface_list
        except Exception as e:
            print(e)

    def object_obj_delete_btn_pressed(self):
        try:
            delete_obj_type_by_id(self.engine, self.object_object_list_select_item.id)
            self.object_obj_list_update()
            self.object_interface_list.clear()
            self.object_description_te.clear()
        except Exception as e:
            print(e)

    def object_obj_add_btn_pressed(self):
        name = self.object_add_le.text()
        description = self.object_add_te.toPlainText()
        if name != '' and name is not None:
            if description is None:
                description = ''
            create_some(db_model.DeviceTypeBase(name=name, description=description), self.engine)
            self.object_obj_list_update()
            self.object_add_le.clear()
            self.object_add_te.clear()

    def object_change_interface_btn_pressed(self):
        if self.object_change_mode:
            self.object_change_mode = False
            self.object_get_obj_type_interfaces()
        else:
            self.object_change_mode = True
            self.object_interface_list.clear()
            self.object_interface_list.addItems(self.object_get_all_interface)
        self.object_add_interface_btn.setEnabled(False)
        self.object_delete_interface_btn.setEnabled(False)

    def object_interface_list_selected(self):
        try:
            if self.object_change_mode:
                self.object_add_interface_btn.setEnabled(True)
                self.object_interface_selected = self.object_get_all_interface_parsed[
                    self.object_interface_list.selectedItems()[0].text()]
            else:
                self.object_delete_interface_btn.setEnabled(True)
                self.object_interface_selected = self.object_get_interface_parsed[
                    self.object_interface_list.selectedItems()[0].text()]
        except Exception as e:
            print(e)

    def object_add_interface_btn_pressed(self):
        device_type_id = self.object_object_list_select_item.id
        interface_id = self.object_interface_selected.id
        create_some(db_model.DeviceTypeInterfaceBase(device_type_id=device_type_id, interface_id=interface_id),
                    self.engine)
        self.object_change_interface_btn_pressed()

    def object_delete_interface_btn_pressed(self):
        device_type_id = self.object_object_list_select_item.id
        interface_id = self.object_interface_selected.id
        delete_interface_obj_type_by_id(engine=self.engine, device_type_id=device_type_id, interface_id=interface_id)
        self.object_get_obj_type_interfaces()

    def negative_neg_list_add(self):
        try:
            if self.negative_add_le.text() != '' and self.negative_add_le.text() is not None:
                damage_types = {'Ущерб физическому лицу': 0, 'Ущерб юридическому лицу': 1, 'Ущерб государству': 2}
                create_some(db_model.NegativeResultBase(name=self.negative_add_le.text(), damage_type=damage_types[
                    self.negative_damage_type_cb.currentText()]), engine=self.engine)
                self.negative_neg_list_update()
        except Exception as e:
            print(e)

    def negative_neg_list_delete(self):
        try:
            selected_neg = self.negative_selected
            delete_negative_by_id(self.engine, selected_neg.id)
            self.negative_neg_list_update()
        except Exception as e:
            print(e)

    def negative_neg_list_selected(self):
        try:
            self.negative_delete_btn.setEnabled(True)
            self.negative_selected = self.negative_get_neg_parsed[self.negative_neg_list.selectedItems()[0].text()]
            damage_types = {0: 'Ущерб физическому лицу', 1: 'Ущерб юридическому лицу', 2: 'Ущерб государству'}
            self.negative_damage_type_te.setPlainText(damage_types[self.negative_selected.damage_type])
        except Exception as e:
            print(e)

    def negative_neg_list_update(self):
        self.negative_neg_list.clear()
        self.negative_delete_btn.setEnabled(False)
        self.negative_get_neg = get_all_negatives(self.engine)
        neg_list = []
        for i in self.negative_get_neg:
            neg_list.append(f'{i.name}')
            self.negative_get_neg_parsed[f'{i.name}'] = i
        self.negative_neg_list.addItems(neg_list)

    def threat_object_list_selected(self):
        try:
            if self.threat_change_mode:
                self.threat_object_add_btn.setEnabled(True)
            else:
                self.threat_object_delete_btn.setEnabled(True)
            self.threat_selected_obj = self.threat_object_list.selectedItems()[0].text()
        except IndexError as a:
            print('base', a)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def threat_object_add_btn_clicked(self):
        try:
            threat_id = self.threat_get_ubi_parsed[self.threat_selected_ubi].id
            device_type_id = self.threat_get_all_object_type_parsed[self.threat_selected_obj].id
            create_some(db_model.DeviceTypeThreatBase(threat_id=threat_id, device_type_id=device_type_id), self.engine)
            self.threat_object_change_btn_clicked()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def threat_object_change_btn_clicked(self):
        try:
            if self.threat_change_mode:
                self.threat_object_delete_btn.setEnabled(False)
                self.threat_object_add_btn.setEnabled(False)
                self.threat_parse_obj()
                self.threat_change_mode = False
            else:
                self.threat_object_list.clear()
                self.threat_object_list.addItems(self.threat_get_all_object_type)
                self.threat_change_mode = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

    def threat_object_delete_btn_clicked(self):
        try:
            threat_id = self.threat_get_ubi_parsed[self.threat_selected_ubi].id
            device_type_id = self.threat_get_object_type_parsed[self.threat_selected_obj].id
            delete_threat_device_type(self.engine, threat_id, device_type_id)
            self.threat_parse_obj()
        except Exception as e:
            print(e)

    def get_all_object_type(self):
        obj_list = []
        self.threat_get_all_object_type = get_all_device_type(self.engine)
        for i in self.threat_get_all_object_type:
            obj_list.append(f'{i.name}')
            self.threat_get_all_object_type_parsed[f'{i.name}'] = i
        self.threat_get_all_object_type = obj_list

    def threat_ubi_list_clicked(self, item):
        try:
            self.threat_change_mode = False
            self.threat_selected_ubi = item.text()
            self.threat_get_object_type_parsed.clear()
            self.threat_object_list.clear()
            intruder = {0: 'Отсутствует',
                        1: 'Низкий',
                        2: 'Средний',
                        3: 'Высокий'}
            clicked_item = self.threat_get_ubi_parsed[item.text()]
            self.threat_name_te.setPlainText(clicked_item.name)
            confidentiality = f'Нарушение конфиденциальности: {check_bool(clicked_item.confidentiality)}'
            integrity = f'Нарушение целостности:{check_bool(clicked_item.integrity)}'
            availability = f'Нарушение доступности:{check_bool(clicked_item.availability)}'
            self.threat_description_te.setPlainText(
                f'{clicked_item.description}\n{confidentiality}\n{integrity}\n{availability}')
            self.threat_internal_te.setPlainText(intruder[int(clicked_item.internal_offender)])
            self.threat_external_te.setPlainText(intruder[int(clicked_item.external_offender)])
            self.threat_parse_obj()
        except Exception as e:
            print(e)

    def window_load(self):
        self.stackedWidget.setCurrentWidget(self.default_page)
        #  threat_page
        self.threat_object_delete_btn.setEnabled(False)
        self.threat_object_add_btn.setEnabled(False)
        #  negative_page

    def threat_parse_obj(self):
        try:
            self.threat_object_list.clear()
            clicked_item = self.threat_get_ubi_parsed[self.threat_selected_ubi]
            self.threat_get_object_type = get_object_type_by_ubi_id(self.engine, int(clicked_item.id))
            obj_list = []
            for i in self.threat_get_object_type:
                obj_list.append(f'{i.name}')
                self.threat_get_object_type_parsed[f'{i.name}'] = i
            self.threat_object_list.addItems(obj_list)
        except Exception as e:
            print(e)

    def enable_all_buttons(self):
        self.threat_btn.setEnabled(True)
        self.negative_btn.setEnabled(True)
        self.object_btn.setEnabled(True)
        self.interface_btn.setEnabled(True)
        self.impact_btn.setEnabled(True)
        self.vulnerability_btn.setEnabled(True)
        self.tactic_btn.setEnabled(True)
        self.realization_btn.setEnabled(True)
        self.device_btn.setEnabled(True)
        self.worker_btn.setEnabled(True)
        self.organization_btn.setEnabled(True)
        self.vulnerability_btn.setEnabled(True)
        self.insider_criteria_btn.setEnabled(True)
        self.intruder_btn.setEnabled(True)
