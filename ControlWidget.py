from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QLineEdit, QPushButton, QComboBox


class ControlWidget(QWidget):
    sent_value = pyqtSignal(int, float)

    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)

        self.__dict_acquisition_types = dict()
        self.__dict_acquisition_types["Linear"] = self.__linear
        self.__dict_acquisition_types["Degression"] = self.__degression
        self.__dict_acquisition_types["Degression auf Linear"] = self.__degression_to_linear

        box_layout = QVBoxLayout()

        box_layout.addWidget(QLabel("Anschaffungswert in Euro"))

        self.line_edit_acquisition_value = QLineEdit("50")
        box_layout.addWidget(self.line_edit_acquisition_value)

        box_layout.addWidget(QLabel("Abschreibungsdauer in Jahren"))

        self.line_edit_acquisition_period = QLineEdit("4")
        box_layout.addWidget(self.line_edit_acquisition_period)

        box_layout.addWidget(QLabel("Abschreibungsart"))

        self.__combo_box_acquisition_typ = QComboBox()
        for key in self.__dict_acquisition_types.keys():
            self.__combo_box_acquisition_typ.addItem(key)
        box_layout.addWidget(self.__combo_box_acquisition_typ)

        push_button = QPushButton("Berechnen")
        push_button.released.connect(self.__depreciation)
        box_layout.addWidget(push_button)

        self.__text_browser = QTextBrowser()
        box_layout.addWidget(self.__text_browser)

        self.setLayout(box_layout)

    @pyqtSlot()
    def __depreciation(self):
        current_text = self.__combo_box_acquisition_typ.currentText()

        self.__dict_acquisition_types[current_text]()

    def __linear(self):
        self.__text_browser.append("Lineare Abschreibung")

        years = int(self.line_edit_acquisition_period.text())
        value = float(self.line_edit_acquisition_value.text())

        loos_per_year = value / years

        current_year = 1
        while value > 1.00:
            line = "Restwert im "
            line += str(current_year)
            line += ". Jahr: \t"
            line += "{:5.2f}".format(value)
            line += " Euro"



            self.__text_browser.append(line)

            value -= loos_per_year
            current_year += 1

        line = "Restwert ab dem "
        line += str(current_year)
        line += ". Jahr: \t 1.00 Euro"

        self.__text_browser.append(line)

    def __degression(self):
        self.__text_browser.append("Degressive Abschreibung")

        years = int(self.line_edit_acquisition_period.text())
        value = float(self.line_edit_acquisition_value.text())

        loos_per_year = (1 - 2 / years)
        if loos_per_year < 0.80:
            loos_per_year = 0.80

        current_year = 1
        while years >= current_year:
            line = "Restwert im "
            line += str(current_year)
            line += ". Jahr: \t"
            line += "{:5.2f}".format(value)
            line += " Euro"

            self.__text_browser.append(line)

            value *= loos_per_year
            current_year += 1

        line = "Restwert ab dem "
        line += str(current_year)
        line += ". Jahr: \t 1.00 Euro"

        self.__text_browser.append(line)

    def __degression_to_linear(self):
        self.__text_browser.clear()
        self.__text_browser.append("Degressive auf lineare Abschreibung:")
        self.__text_browser.append("------------------------------------")
        self.__text_browser.append("")

        years = int(self.line_edit_acquisition_period.text())
        linear_value = degressiv_value = float(self.line_edit_acquisition_value.text())

        linear_loos_per_year = linear_value / years

        degressiv_loos_per_year = 2 / years
        if degressiv_loos_per_year < 0.20:
            degressiv_loos_per_year = 0.20


        self.__text_browser.append("Jahr\tBuchwert\tAbschreibung\tArt")

        current_year = 1
        while True:
            if linear_loos_per_year > (degressiv_value * degressiv_loos_per_year):
                break

            line = str(current_year)
            line += "\t"
            line += "{:5.2f}".format(degressiv_value)
            line += "\t"
            line += "{:5.2f}".format(degressiv_value * degressiv_loos_per_year)
            line += "\t\tdegressiv"

            self.__text_browser.append(line)

            self.sent_value.emit(current_year, degressiv_value)

            linear_value -= linear_loos_per_year
            degressiv_value *= (1 - degressiv_loos_per_year)

            current_year += 1

        while degressiv_value > linear_loos_per_year:
            line = str(current_year)
            line += "\t"
            line += "{:5.2f}".format(degressiv_value)
            line += "\t"
            line += "{:5.2f}".format(linear_loos_per_year)
            line += "\t\tlinear"

            self.sent_value.emit(current_year, degressiv_value)

            self.__text_browser.append(line)

            current_year += 1
            degressiv_value -= linear_loos_per_year

        line = "Ab "
        line += str(current_year)
        line += "\t1,00\t0,00\t\tkeine"

        self.sent_value.emit(current_year, 1.00)

        self.__text_browser.append(line)


