from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from ChartWidget import ChartWidget
from ControlWidget import ControlWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        control_widget = ControlWidget(self)
        chart_widget = ChartWidget(self)

        box_layout = QHBoxLayout()

        box_layout.addWidget(control_widget)
        box_layout.addWidget(chart_widget)

        self.setLayout(box_layout)
