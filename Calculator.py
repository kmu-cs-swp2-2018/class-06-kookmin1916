from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Button(QToolButton):
    def __init__(self, text, callback):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(self.display, 0, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("My Calculator")

        self.decButton = Button(".", self.buttonClicked)
        self.eqButton = Button("=", self.buttonClicked)
        self.digitButton = [x for x in range(0, 10)]
        self.opButton = [x for x in range(0, 7)]
        self.opList = ["*", "/", "+", "-", "(", ")", "C"]

        for i in range(10):
            self.digitButton[i] = Button(str(i), self.buttonClicked)
        for i in range(7):
            self.opButton[i] = Button(self.opList[i], self.buttonClicked)
        # for i in range(10):
        #    self.digitButton[i] = QToolButton()
        #    self.digitButton[i].setText(str(i))

        numLayout = QGridLayout()
        numLayout.setSizeConstraint(QLayout.SetFixedSize)
        for i in range(9):
            numLayout.addWidget(self.digitButton[9 - i], i // 3, 2 - i % 3, 1, 1)
        numLayout.addWidget(self.digitButton[0], 3, 0)
        numLayout.addWidget(self.decButton, 3, 1)
        numLayout.addWidget(self.eqButton, 3, 2)

        opLayout = QGridLayout()
        for i in range(7):
            opLayout.addWidget(self.opButton[i], i // 2, i % 2)

        mainLayout.addLayout(numLayout, 1, 0)
        mainLayout.addLayout(opLayout, 1, 1)

    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        if key == '=':
            result = str(eval(self.display.text()))
            self.display.setText(result)
        elif key == 'C':
            self.display.setText("")
        else:
            self.display.setText(self.display.text() + key)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
