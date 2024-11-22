from datetime import datetime

from PyQt6.QtCharts import QChartView, QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import Qt, QDateTime, pyqtSlot
from PyQt6.QtGui import QMouseEvent


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super(ChartWidget, self).__init__(parent)

        self.__series = QLineSeries()
        self.__series.setName("Restwert")

        self.__axis_x = QDateTimeAxis()
        self.__axis_x.setTitleText("Datum")
        self.__axis_x.setFormat("yyyy")

        self.__axis_dollar = QValueAxis()
        self.__axis_dollar.setTitleText("Restwert")

        self.__chart = QChart()
        self.__chart.setTitle("Abschreibungsverlauf")

        self.__chart.addAxis(self.__axis_x, Qt.AlignmentFlag.AlignBottom)
        self.__chart.addAxis(self.__axis_dollar, Qt.AlignmentFlag.AlignLeft)

        self.__chart.addSeries(self.__series)

        self.__series.attachAxis(self.__axis_x)
        self.__series.attachAxis(self.__axis_dollar)

        self.setChart(self.__chart)

    @pyqtSlot(str)
    def setYears(self, years):
        start_date = QDateTime.currentDateTime()
        end_date = QDateTime.currentDateTime().addYears(int(years))

        self.__axis_x.setRange(start_date, end_date)

    @pyqtSlot(str)
    def setValue(self, value):
        self.__axis_dollar.setRange(0, float(value))

    @pyqtSlot(int, float)
    def addPoint(self, year, value):
        current_date_time = QDateTime.currentDateTime().addYears(year)
        print(current_date_time, value)

        self.__series.append(current_date_time.toMSecsSinceEpoch(), value)
