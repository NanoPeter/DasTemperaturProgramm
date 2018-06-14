#!/usr/bin/python3
from scientificdevices.lakeshore.model340 import Model340, Loop
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFormLayout, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QLabel, QPushButton, QWidget,
                             QCheckBox, QMessageBox)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DasTemperaturProgramm')
        self._init_ui()
        self._init_device()

    def _init_ui(self):
        central_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        
        form_widget = self._init_form(central_widget)
        okay_widget = self._init_okay_button(central_widget)

        central_layout.addWidget(form_widget)
        central_layout.addStretch(1)
        central_layout.addWidget(okay_widget)
        self.setCentralWidget(central_widget)

    def _init_form(self, central_widget):
        form_widget = QWidget(central_widget)
        form_widget_layout = QFormLayout()  
        form_widget.setLayout(form_widget_layout)

        self._temperature_input = QLineEdit(form_widget)
        self._ramp = QLineEdit(form_widget)
        self._ramp_enabled = QCheckBox('', form_widget)

        form_widget_layout.addRow(QLabel('Set Temperature[K]'), self._temperature_input)
        form_widget_layout.addRow(QLabel('Ramp [K/min]'), self._ramp)
        form_widget_layout.addRow(QLabel('Ramp Enabled'), self._ramp_enabled)

        return form_widget

    def _init_okay_button(self, central_widget):
        okay_widget = QWidget(central_widget)
        okay_widget_layout = QHBoxLayout()
        okay_widget.setLayout(okay_widget_layout)

        okay_button = QPushButton('set', okay_widget)

        okay_button.clicked.connect(self._set_button_clicked)

        okay_widget_layout.addStretch(1)
        okay_widget_layout.addWidget(okay_button)

        return okay_widget    

    def _init_device(self):
        self._controller = Model340(address=12)

        ramp_parameter = self._controller.get_ramp()
        set_point = self._controller.get_set_point()

        self._temperature_input.setText(str(round(set_point,4)))
        self._ramp.setText(str(round(ramp_parameter['rate'], 2)))
        self._ramp_enabled.setChecked(ramp_parameter['enabled'])

    def _set_button_clicked(self):
        temperature = self._controller.get_temperature()
        set_point = float(self._temperature_input.text())
        ramp = float(self._ramp.text())
        ramp_enabled = self._ramp_enabled.isChecked()

        if not (0 <= set_point <= 295):
            print('Error: set point out of range.')
            return

        if not (0 <= ramp <= 2.5):
            print('Error: ramp out of range.')
            return

        if abs(set_point - temperature) > 10 and not ramp_enabled:
            result = QMessageBox.question(self, 'Set point to far away', 
                                          ('New set point temperature is too far away from current temperature.'
                                           'This can cause overshooting.'
                                           'Are you sure you want to continue without enabling a ramp?'
                                          ),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                                         )
            if result == QMessageBox.No:
                return
                
        self._controller.set_ramp(enable=ramp_enabled, rate=ramp)
        self._controller.set_set_point(set_point)

        
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())

