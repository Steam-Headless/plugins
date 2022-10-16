# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from . import common


class GuiMainWindow(object):

    def __init__(self):
        # Read config
        self.config = common.read_config()
        print(self.config)

        # UI Components
        self.centralwidget = None
        self.horizontalLayout = None

        self.groupBox = None

        # Settings
        self.enable_toggles = {}

        # Actions
        self.apply_button = None

        self.enabled_services = []

    def save_config(self):
        for key in self.enable_toggles:
            self.config["services"][key]["enabled"] = self.enable_toggles.get(key).isChecked()
        # Save changes
        common.write_config(self.config)

    def setup_layouts(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")

    def gettext(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        if ok:
            self.le1.setText(str(text))

    def add_enable_services_checkboxes(self):
        new_group_box = QtWidgets.QGroupBox;()
        layout = QtWidgets.QVBoxLayout(new_group_box)
        configured_services = self.config.get('services', {})
        for key in common.all_services:
            service = common.all_services.get(key)
            service_name = service.get("name")
            current_config = configured_services.get(key, {})
            self.enable_toggles[key] = QtWidgets.QCheckBox(new_group_box)
            self.enable_toggles[key].setText("Enable %s" % service_name)
            self.enable_toggles[key].setChecked(current_config.get('enabled', False))
            self.enable_toggles[key].stateChanged.connect(self.save_config)
            layout.addWidget(self.enable_toggles[key])

            if service.get("multi"):
                print(1234)
                btn2 = QtWidgets.QPushButton("Enter an integer")
                btn2.clicked.connect(self.getint)
                roll, done2 = QtWidgets.QInputDialog.getInt(
                    self, 'Input Dialog', 'Enter your roll:')
                # slider = QtWidgets.QSlider(new_group_box)
                # slider.setObjectName("multi_service_counter")
                # slider.setOrientation(QtCore.Qt.Horizontal)
                # layout.addWidget(slider)
        self.verticalLayout.addWidget(new_group_box)

    def setup_config_items(self):
        self.add_enable_services_checkboxes()

        # Add apply button
        self.apply_button = QtWidgets.QPushButton(self.groupBox)
        self.apply_button.setObjectName("apply_button")
        self.apply_button.setText("Apply")
        self.verticalLayout.addWidget(self.apply_button)

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(893, 606)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Select an update channel")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")

        # Set up the config items
        self.setup_config_items()

        # Add a spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("UpdateWindow")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def old_setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(893, 606)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Select an update channel")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")

        self.radio_1 = QtWidgets.QRadioButton(self.groupBox)
        self.radio_1.setObjectName("radio_1")
        self.radio_1.setText("Stabled")
        self.verticalLayout.addWidget(self.radio_1)
        self.radio_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radio_2.setObjectName("radio_2")
        self.radio_2.setText("Beta")
        self.verticalLayout.addWidget(self.radio_2)
        self.add_button = QtWidgets.QPushButton(self.groupBox)
        self.add_button.setObjectName("add_button")
        self.add_button.setText("Download/Install Updates")
        self.verticalLayout.addWidget(self.add_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)

        self.list_widget = QtWidgets.QListWidget(self.centralwidget)
        self.list_widget.setObjectName("list_widget")
        self.horizontalLayout.addWidget(self.list_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        MainWindow.setWindowTitle("UpdateWindow")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GuiMainWindow()
        self.ui.setup_ui(self)

        self.ui.apply_button.clicked.connect(self.exec_update)

    def get_radio_option(self):
        if self.ui.radio_1.isChecked():
            return 'stable'
        elif self.ui.radio_2.isChecked():
            return 'beta'
        return None

    def exec_update(self):
        channel = self.get_radio_option()
        if channel is None:
            QtWidgets.QListWidgetItem('Select an update channel!', self.ui.list_widget)
            return
        # TODO: Exec docker compose commands
        docker_compose_command = []
        proc, sp = common.exec_process(docker_compose_command)
        text = ' '.join(sp.stdout.readlines())
        QtWidgets.QListWidgetItem(text, self.ui.list_widget)


def show_window():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
