# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py_ui/AuthWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthWindow(object):
    def setupUi(self, AuthWindow):
        AuthWindow.setObjectName("AuthWindow")
        AuthWindow.resize(800, 600)
        AuthWindow.setMinimumSize(QtCore.QSize(800, 600))
        AuthWindow.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        AuthWindow.setFont(font)
        AuthWindow.setStyleSheet("QLineEdit {\n"
"  border-radius: 8px;\n"
"  border: 1px solid #e0e4e7;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"  border: 1px solid #d0e3ff;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"  color: #767e89;\n"
"}\n"
"\n"
"QGroupBox {\n"
"background-color: rgb(205, 205, 205);\n"
"border: 3px solid rgb(154, 154, 154);\n"
"border-radius: 40px;\n"
"}\n"
"QGroupBox::title{\n"
"}\n"
"QPushButton{border-radius: 8px;background-color: rgb(255, 255, 255);}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(205, 205, 205);\n"
"  border: 3px solid #9ac3fe;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:rgb(128, 128, 128);\n"
"   border: 3px solid #9ac3fe;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(AuthWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.intro_lbl = QtWidgets.QLabel(self.centralwidget)
        self.intro_lbl.setGeometry(QtCore.QRect(0, 90, 801, 91))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.intro_lbl.setFont(font)
        self.intro_lbl.setStyleSheet("QLabel {background-color: rgb(205, 205, 205)}")
        self.intro_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_lbl.setObjectName("intro_lbl")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(200, 210, 400, 261))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet("")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.port_le = QtWidgets.QLineEdit(self.groupBox)
        self.port_le.setGeometry(QtCore.QRect(220, 110, 61, 31))
        self.port_le.setStyleSheet("")
        self.port_le.setText("")
        self.port_le.setObjectName("port_le")
        self.password_le = QtWidgets.QLineEdit(self.groupBox)
        self.password_le.setGeometry(QtCore.QRect(120, 70, 161, 31))
        self.password_le.setStyleSheet("")
        self.password_le.setInputMask("")
        self.password_le.setText("")
        self.password_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_le.setObjectName("password_le")
        self.ip_address_le = QtWidgets.QLineEdit(self.groupBox)
        self.ip_address_le.setGeometry(QtCore.QRect(120, 110, 91, 31))
        self.ip_address_le.setStyleSheet("")
        self.ip_address_le.setInputMask("")
        self.ip_address_le.setText("")
        self.ip_address_le.setObjectName("ip_address_le")
        self.log_in_btn = QtWidgets.QPushButton(self.groupBox)
        self.log_in_btn.setGeometry(QtCore.QRect(130, 200, 141, 51))
        self.log_in_btn.setStyleSheet("")
        self.log_in_btn.setObjectName("log_in_btn")
        self.login_le = QtWidgets.QLineEdit(self.groupBox)
        self.login_le.setGeometry(QtCore.QRect(120, 30, 161, 31))
        self.login_le.setStyleSheet("")
        self.login_le.setText("")
        self.login_le.setObjectName("login_le")
        self.db_name_le = QtWidgets.QLineEdit(self.groupBox)
        self.db_name_le.setGeometry(QtCore.QRect(120, 150, 161, 31))
        self.db_name_le.setStyleSheet("")
        self.db_name_le.setReadOnly(False)
        self.db_name_le.setObjectName("db_name_le")
        self.notification_lbl = QtWidgets.QLabel(self.centralwidget)
        self.notification_lbl.setGeometry(QtCore.QRect(200, 480, 401, 71))
        self.notification_lbl.setText("")
        self.notification_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.notification_lbl.setWordWrap(True)
        self.notification_lbl.setObjectName("notification_lbl")
        AuthWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AuthWindow)
        QtCore.QMetaObject.connectSlotsByName(AuthWindow)

    def retranslateUi(self, AuthWindow):
        _translate = QtCore.QCoreApplication.translate
        AuthWindow.setWindowTitle(_translate("AuthWindow", "MainWindow"))
        self.intro_lbl.setText(_translate("AuthWindow", "Моделирование угроз"))
        self.groupBox.setTitle(_translate("AuthWindow", "Подключение к базе данных"))
        self.port_le.setPlaceholderText(_translate("AuthWindow", "Порт"))
        self.password_le.setPlaceholderText(_translate("AuthWindow", "Пароль"))
        self.ip_address_le.setPlaceholderText(_translate("AuthWindow", "IP-адрес"))
        self.log_in_btn.setText(_translate("AuthWindow", "Подключиться"))
        self.login_le.setPlaceholderText(_translate("AuthWindow", "Логин"))
        self.db_name_le.setPlaceholderText(_translate("AuthWindow", "Имя базы данных"))
