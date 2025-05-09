from data_base import db_model
from data_base.db_controller import get_all_some, get_impact_types_by_dev_id, get_ubi_by_dev_id, get_negative_by_dev_id, get_realization_by_dev_id, get_vul_by_dev_id, get_scenario_by_dev_id_threat_id
from py_ui.ui_EngineerWindow import Ui_EngineerWindow
from PyQt5 import QtWidgets
from functions import functions


class EngineerWindow(QtWidgets.QMainWindow, Ui_EngineerWindow):
    def __init__(self, engine):
        try:
            super().__init__()
            self.setupUi(self)
            self.engine = engine

            self.devices_parsed = {}
            devices = get_all_some(self.engine, db_model.DeviceBase)

            self.devices = []
            for i in devices:
                self.devices.append(f'{i.id} | {i.ip_address}')
                self.devices_parsed[f'{i.id} | {i.ip_address}'] = i
            self.device_list.addItems(self.devices)
            self.device_list.itemSelectionChanged.connect(self.device_list_selected)
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
        except Exception as e:
            print(e)

    def device_list_selected(self):
        try:
            a = self.device_list.selectedItems()[0].text()
            self.dev_selected = self.devices_parsed[a]

            self.impact_parsed.clear()
            self.impact = get_impact_types_by_dev_id(self.engine, self.dev_selected.id)
            impact = []
            for i in self.impact:
                impact.append(f'{i.name}')
                self.impact_parsed[f'{i.name}'] = i
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
            self.impact = get_negative_by_dev_id(self.engine, self.dev_selected.id)
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

        self.scenario_parsed.clear()
        self.scenario = get_scenario_by_dev_id_threat_id(self.engine, self.dev_selected.id, self.ubi_selected[0])
        scenario = []
        for i in self.scenario:
            scenario.append(f'{i[1]} | {i[2]}')
            self.scenario_parsed[f'{i[1]} | {i[2]}'] = i
        self.scenario = scenario
        self.tactic_technique_list.addItems(self.scenario)

