from PyQt5.QtGui import QIcon
from py_ui.ui_AuthWindow import Ui_AuthWindow
from view.admin_window import AdminWindow
from view.engineer_window import EngineerWindow
from PyQt5 import QtWidgets
from sqlalchemy import create_engine
from data_base.db_controller import get_user_role


class AuthWindow(QtWidgets.QMainWindow, Ui_AuthWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Подключение')
            self.setWindowIcon(QIcon('files/lock.ico'))
            self.log_in_btn.pressed.connect(self.log_in)
        except Exception as e:
            print(e)

    def log_in(self):
        try:
            #SQLALCHEMY_DATABASE_URL = f"postgresql://{self.login_le.text()}:{self.password_le.text()}@{self.ip_address_le.text()}:{self.port_le.text()}/{self.db_name_le.text()}"
            SQLALCHEMY_DATABASE_URL = f"postgresql://{self.login_le.text()}:kali@192.168.226.152:5432/postgres"
            engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
            engine.connect()
            self.notification_lbl.setText('Соединение установлено')
            role = get_user_role(engine, self.login_le.text())
            if role.role == 0:
                admin_window = AdminWindow(engine)
                self.window = admin_window
                self.window.show()
                self.close()
            elif role.role == 1:
                engineer_window = EngineerWindow(engine)
                self.window = engineer_window
                self.window.show()
                self.close()
        except Exception as e:
            self.notification_lbl.setText(f'Ошибка подключения\n{e}')

