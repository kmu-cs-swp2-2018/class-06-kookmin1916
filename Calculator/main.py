from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Calculator.Functional import *
from Calculator.Constant import *

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

        functionLayout = QGridLayout()
        functionLayout.setSizeConstraint(QLayout.SetFixedSize)
        for i in range(len(functionList)):
            functionLayout.addWidget(Button(functionList[i][0], self.buttonClicked), i, 0)

        constantLayout = QGridLayout()
        constantLayout.setSizeConstraint(QLayout.SetFixedSize)
        for i in range(len(constantList)):
            constantLayout.addWidget(Button(constantList[i][0], self.buttonClicked), i, 0)

        mainLayout.addLayout(numLayout, 1, 0)
        mainLayout.addLayout(opLayout, 1, 1)
        mainLayout.addLayout(functionLayout, 2, 1)
        mainLayout.addLayout(constantLayout, 2, 0)

    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        try:
            if key == '=':
                result = str(eval(self.display.text()))
                self.display.setText(result)
            elif key == 'C':
                self.display.setText("")
            else:
                for i in functionList:
                    if key == i[0]:
                        self.display.setText(str(i[1](self.display.text())))
                        return
                for i in constantList:
                    if key == i[0]:
                        if self.display.text() == "" or self.display.text() == "Error":
                            self.display.setText(str(i[1]))
                        else:
                            self.display.setText(self.display.text() + "*" + str(i[1]))
                        return
                if self.display.text() == "Error":
                    self.display.setText(key)
                else:
                    self.display.setText(self.display.text() + key)
        except:
            self.display.setText("Error")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
