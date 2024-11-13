from PyQt6.QtCharts import QChartView, QChart, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QMouseEvent


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super(ChartWidget, self).__init__(parent)

        self.__series = QLineSeries()
        self.__series.setName("Goldpreisentwicklung in $")

        axis_x = QDateTimeAxis()
        axis_x.setTitleText("Datum")

        start_date = QDateTime.currentDateTime().addSecs(-1 * 60 * 10)
        end_date = QDateTime.currentDateTime()

        axis_x.setRange(start_date, end_date)

        axis_x.setFormat("hh:mm:ss")

        axis_dollar = QValueAxis()
        axis_dollar.setTitleText("Goldpreis in $")
        axis_dollar.setRange(1250, 2750)

        self.__chart = QChart()
        self.__chart.setTitle("Goldpreisentwicklung")

        self.__chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.__chart.addAxis(axis_dollar, Qt.AlignmentFlag.AlignLeft)

        self.__chart.addSeries(self.__series)

        self.__series.attachAxis(axis_x)
        self.__series.attachAxis(axis_dollar)

        self.setChart(self.__chart)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button().LeftButton:
            event.accept()

            new_value = self.__chart.mapToValue(event.pos().toPointF(), self.__series)

            for i in range(len(self.__series.points())):
                if self.__series.at(i).x() > new_value.x():
                    self.__series.insert(i, new_value)

                    return

            self.__series.append(new_value)

