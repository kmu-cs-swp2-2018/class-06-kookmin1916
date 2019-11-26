# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QLabel

from HangmanGame.Hangman import Hangman
from HangmanGame.Guess import Guess
from HangmanGame.Word import Word


class HangmanGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize word database
        self.word = Word('words.txt')

        # Hangman display window
        self.hangmanWindow = QTextEdit()
        self.hangmanWindow.setReadOnly(True)
        self.hangmanWindow.setAlignment(Qt.AlignLeft)
        font = self.hangmanWindow.font()
        font.setFamily('Courier New')
        self.hangmanWindow.setFont(font)

        # Layout
        hangmanLayout = QGridLayout()
        hangmanLayout.addWidget(self.hangmanWindow, 0, 0)

        # Status Layout creation
        statusLayout = QGridLayout()

        # Display widget for current status
        self.currentWord = QLineEdit()
        self.currentWord.setReadOnly(True)
        self.currentWord.setAlignment(Qt.AlignCenter)
        font = self.currentWord.font()
        font.setPointSize(font.pointSize() + 8)
        self.currentWord.setFont(font)
        #self.currentWord.setMaxLength(4)
        self.currentWord.setFixedWidth(300)
        statusLayout.addWidget(self.currentWord, 0, 0, 1, 2)

        # Display widget for already used characters
        self.guessedChars = QLineEdit()
        self.guessedChars.setReadOnly(True)
        self.guessedChars.setAlignment(Qt.AlignLeft)
        self.guessedChars.setMaxLength(52)
        statusLayout.addWidget(self.guessedChars, 1, 0, 1, 2)

        # Display widget for message output
        self.message = QLineEdit()
        self.message.setReadOnly(True)
        self.message.setAlignment(Qt.AlignLeft)
        self.message.setMaxLength(52)
        statusLayout.addWidget(self.message, 2, 0, 1, 2)

        # Input widget for user selected characters
        self.charInput = QLineEdit()
        self.charInput.setMaxLength(1)
        statusLayout.addWidget(self.charInput, 3, 0)

        # Button for submitting a character
        self.guessButton = QToolButton()
        self.guessButton.setText('Guess!')
        self.guessButton.clicked.connect(self.guessClicked)
        statusLayout.addWidget(self.guessButton, 3, 1)

        # Button for a new game
        self.newGameButton = QToolButton()
        self.newGameButton.setText('New Game')
        self.newGameButton.clicked.connect(self.startGame)
        statusLayout.addWidget(self.newGameButton, 4, 0)

        # Display widget for input min/max length text
        min_length_text = QLabel()
        min_length_text.setAlignment(Qt.AlignRight)
        min_length_text.setText("min length :")
        statusLayout.addWidget(min_length_text, 5, 0)

        max_length_text = QLabel()
        max_length_text.setAlignment(Qt.AlignRight)
        max_length_text.setText("max length :")
        statusLayout.addWidget(max_length_text, 6, 0)
        
        # Input widget for min/max length of words
        self.minLengthInput = QLineEdit()
        #self.minLengthInput.setMaxLength(1)
        statusLayout.addWidget(self.minLengthInput, 5, 1)

        self.maxLengthInput = QLineEdit()
        #self.maxLengthInput.setMaxLength(1)
        statusLayout.addWidget(self.maxLengthInput, 6, 1)

        # Layout placement
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(hangmanLayout, 0, 0)
        mainLayout.addLayout(statusLayout, 0, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle('Hangman Game')

        # Start a new game on application launch!
        self.startGame()

    def startGame(self):
        self.hangman = Hangman()

        min_length = self.minLengthInput.text()
        max_length = self.maxLengthInput.text()
        if min_length == "":
            min_length = "1"
        if max_length == "":
            max_length = "100"

        if not min_length.isdigit() or not max_length.isdigit() or\
                int(min_length) <= 0 or int(max_length) <= 0:
            self.message.setText("Please Enter a Positive Integer")
            return

        picked_word = self.word.randFromDB(int(min_length), int(max_length))
        if picked_word is None:
            self.message.setText("No Words Found")
            return

        self.guess = Guess(picked_word)
        self.gameOver = False

        self.hangmanWindow.setPlaceholderText(self.hangman.current_shape())
        self.currentWord.setText(self.guess.displayCurrent())
        self.guessedChars.setText(self.guess.displayGuessed())
        self.message.clear()

    def guessClicked(self):
        guessedChar = self.charInput.text().lower()
        self.charInput.clear()
        self.message.clear()
        if self.gameOver is True:
            self.message.setText("Please Start New Game")
            return
            # 메시지 출력하고 - message.setText() - 리턴

        if len(guessedChar) != 1:
            self.message.setText("Please Enter a Character")
            return
        # 입력의 길이가 1 인지를 판단하고, 아닌 경우 메시지 출력, 리턴

        for char in self.guess.guessedChars:
            if char == guessedChar:
                self.message.setText("Please Enter New Character")
                return
        # 이미 사용한 글자인지를 판단하고, 아닌 경우 메시지 출력, 리턴

        if not guessedChar.isalpha():
            self.message.setText("Please Enter an Alphabet")
            return

        success = self.guess.guess(guessedChar)
        if success == False:
            self.hangman.life_decrease()
            self.message.setText(str(self.hangman.get_life()) + " Lives Remain")
            # 메시지 출력
        else:
            self.message.setText("Correct!")

        self.hangmanWindow.setPlaceholderText(self.hangman.current_shape())
        # hangmanWindow 에 현재 hangman 상태 그림을 출력
        self.currentWord.setText(self.guess.displayCurrent())
        # currentWord 에 현재까지 부분적으로 맞추어진 단어 상태를 출력
        self.guessedChars.setText(self.guess.displayGuessed())
        # guessedChars 에 지금까지 이용한 글자들의 집합을 출력

        if self.guess.finished():
            self.message.setText("Success!")
            self.gameOver = True
            # 메시지 ("Success!") 출력하고, self.gameOver 는 True 로

        elif self.hangman.get_life() == 0:
            self.message.setText("Fail! - " + self.guess.secretWord)
            self.gameOver = True
            # 메시지 ("Fail!" + 비밀 단어) 출력하고, self.gameOver 는 True 로


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())

