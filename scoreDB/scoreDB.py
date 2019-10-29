import pickle
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

dbfilename = 'scoreDB.dat'


def readScoreDB():
    try:
        fH = open(dbfilename, 'rb')
    except FileNotFoundError as e:
        print("New DB: ", dbfilename)
        return []

    scdb = []
    try:
        scdb = pickle.load(fH)
    except:
        print("Empty DB: ", dbfilename)
    else:
        print("Open DB: ", dbfilename)
    fH.close()
    return scdb


def writeScoreDB(scdb):
    fH = open(dbfilename, 'wb')
    pickle.dump(scdb, fH)
    fH.close()


class ScoreDBWindow(QWidget):
    def __init__(self, scdb):
        super().__init__()
        self._scdb = scdb
        self._line_edits = []
        self._text_edit = QTextEdit(self)
        self._combo_box = QComboBox(self)
        self.initUI()

    def initUI(self):
        hbox = []
        line_cnt = -1

        strings_of_input_cells = ["Name: ", "Age: ", "Score: ", "Amount: "]
        input_cells = []
        for i in range(4):
            self._line_edits.append(QLineEdit(self))
            input_cells.append([QLabel(strings_of_input_cells[i], self),
                                self._line_edits[i]])

        hbox.append(QHBoxLayout())
        line_cnt += 1
        for i in range(3):
            hbox[line_cnt].addWidget(input_cells[i][0])
            hbox[line_cnt].addWidget(input_cells[i][1])

        hbox.append(QHBoxLayout())
        line_cnt += 1
        hbox[line_cnt].addStretch(1)
        hbox[line_cnt].addWidget(input_cells[3][0])
        hbox[line_cnt].addWidget(input_cells[3][1])

        hbox[line_cnt].addWidget(QLabel("Key: "))
        self._combo_box.addItems(["Name", "Age", "Score"])
        hbox[line_cnt].addWidget(self._combo_box)

        hbox.append(QHBoxLayout())
        line_cnt += 1
        strings_of_buttons = ["Add", "Del", "Find", "Inc", "Show"]
        for str in strings_of_buttons:
            button = QPushButton(str, self)
            hbox[line_cnt].addWidget(button)
            button.clicked.connect(self.buttonClicked)

        hbox.append(QHBoxLayout())
        line_cnt += 1
        hbox[line_cnt].addWidget(QLabel("Result:", self))

        hbox.append(QHBoxLayout())
        line_cnt += 1
        hbox[line_cnt].addWidget(self._text_edit)

        vbox = QVBoxLayout()
        for i in hbox:
            vbox.addLayout(i)

        self.setLayout(vbox)
        self.setWindowTitle("Score DB")
        self.showScoreDB()
        self.show()

    def closeEvent(self, event):
        clicked_button = QMessageBox.question(self, "종료", "정말 끄시겠습니까?",
                                              QMessageBox.Yes | QMessageBox.No)
        if clicked_button == QMessageBox.Yes:
            writeScoreDB(self._scdb)
            event.accept()
        else:
            event.ignore()

    def showScoreDB(self, finding_name=None):
        output_string = ""

        if finding_name is None:
            filtered_scdb = self._scdb
        else:
            filtered_scdb = list(filter(lambda data: data["Name"] == finding_name, self._scdb))

        for p in sorted(filtered_scdb, key=lambda person: person[self._combo_box.currentText()]):
            for attr in sorted(p):
                output_string += attr + "=" + p[attr] + "\t\t"
            output_string += "\n"
        self._text_edit.setPlainText(output_string)

    def buttonClicked(self):
        sender = self.sender()
        clicked_button = sender.text()
        name, age, score, amount = [line_edit.text() for line_edit in self._line_edits]
        if clicked_button == "Add":
            self._scdb += [{'Name': name, 'Age': age, 'Score': score}]
            self.showScoreDB()

        elif clicked_button == "Del":
            self._scdb = list(filter(lambda data: data["Name"] != name, self._scdb))
            self.showScoreDB()

        elif clicked_button == "Find":
            self.showScoreDB(name)

        elif clicked_button == "Inc":
            for score_data in self._scdb:
                if score_data["Name"] == name:
                    score_data["Score"] = str(int(score_data["Score"]) + int(amount))
            self.showScoreDB()

        elif clicked_button == "Show":
            self.showScoreDB()


if __name__ == "__main__":
    scoredb = readScoreDB()
    app = QApplication(sys.argv)
    window = ScoreDBWindow(scoredb)
    sys.exit(app.exec_())
