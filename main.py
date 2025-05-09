import sys

import PyQt5.QtWidgets as QtWidgets
from view.auth_window import AuthWindow

from data_base.db_model import create_db
from sqlalchemy import create_engine
# SQLALCHEMY_DATABASE_URL = "postgresql://kali:kali@192.168.226.152:5432/postgres"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# create_db(engine)

# pyuic5 py_ui/AuthWindow.ui -o py_ui/ui_AuthWindow.py
# pyuic5 py_ui/AdminWindow.ui -o py_ui/ui_AdminWindow.py
# pyuic5 py_ui/EngineerWindow.ui -o py_ui/ui_EngineerWindow.py

# GRANT ALL PRIVILEGES ON SCHEMA public TO a;
# GRANT ALL PRIVILEGES ON ALL TABLES    IN SCHEMA public TO a;
# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO a;

from functions import ubi_parsing, vul_parsing
from deployment import test_filling


def vul_parse(engine):
    vul_parsing.download_vul_file()
    vul_parsing.parse_vulnerabilities(engine)
    vul_parsing.parse_software_types_and_vul_types(engine)
    vul_parsing.connect_vul_soft_vul_type(engine)


def ubi_parse(engine):
    ubi_parsing.download_ubi_file()
    ubi_parsing.parse_device_types(engine)
    ubi_parsing.parse_ubi_threats(engine)
    ubi_parsing.connect_treat_device_type(engine)


def test_fill(engine):
    test_filling.negative(engine)
    test_filling.realization(engine)
    test_filling.devices(engine)
    test_filling.device_result(engine)
    test_filling.device_threat(engine)
    test_filling.device_realization(engine)
    test_filling.impact_types(engine)
    test_filling.interface_fill(engine)
    test_filling.interface_realization_fill(engine)
    test_filling.device_type_interface(engine)
    test_filling.tactic_and_technique(engine)
    test_filling.device_scenario(engine)
    test_filling.organization_fill(engine)
    test_filling.intruders(engine)
    test_filling.insider_criteria_fill(engine)
    test_filling.device_connection(engine)
    test_filling.device_vul(engine)


def re_create():
    SQLALCHEMY_DATABASE_URL = "postgresql://kali:kali@192.168.226.152:5432/postgres"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    create_db(engine)
    vul_parse(engine)
    ubi_parse(engine)
    test_fill(engine)


# threat_model.create_threat_model(engine)
def main():

    try:
        app = QtWidgets.QApplication(sys.argv)
        auth_window = AuthWindow()
        window = auth_window
        window.show()
        app.exec_()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
