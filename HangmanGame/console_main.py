# -*- coding: utf-8 -*-

from Hangman import Hangman
from Guess import Guess
from Word import Word


class HangmanGame:

    def __init__(self):
        # Initialize word database
        self.word = Word('words.txt')

        # Start a new game on application launch!
        self.startGame()

    def startGame(self):
        while True:
            picked_word = None
            while True:
                self.hangman = Hangman()

                min_length = input("Enter Minimum Length : ")
                max_length = input("Enter Maximum Length : ")

                if not min_length.isdigit() or not max_length.isdigit() or\
                        int(min_length) <= 0 or int(max_length) <= 0:
                    print("Please Enter a Positive Integer")
                    continue

                picked_word = self.word.randFromDB(int(min_length), int(max_length))
                if picked_word is None:
                    print("No Words Found")
                    continue
                break
            self.guess = Guess(picked_word)
            self.gameOver = False
            while not self.gameOver:
                self.guessClicked()

    def guessClicked(self):
        guessedChar = input("Enter a Character : ")
        guessedChar = guessedChar.lower()
        if self.gameOver is True:
            print("Please Start New Game")
            return

        if len(guessedChar) != 1:
            print("Please Enter a Character")
            return

        for char in self.guess.guessedChars:
            if char == guessedChar:
                print("Please Enter New Character")
                return

        if not guessedChar.isalpha():
            print("Please Enter an Alphabet")
            return

        success = self.guess.guess(guessedChar)
        if success == False:
            self.hangman.life_decrease()
            print(str(self.hangman.get_life()) + " Lives Remain")
            # 메시지 출력
        else:
            print("Correct!")

        print(self.hangman.current_shape())
        # 현재 hangman 상태 그림을 출력
        print("Current : ", (self.guess.displayCurrent()))
        # 현재까지 부분적으로 맞추어진 단어 상태를 출력
        print("Guessed Characters : ", (self.guess.displayGuessed()))
        # 지금까지 이용한 글자들의 집합을 출력
        print("Lives : ", str(self.hangman.get_life()))

        if self.guess.finished():
            print("Success!")
            self.gameOver = True
            # 메시지 ("Success!") 출력하고, self.gameOver 는 True 로

        elif self.hangman.get_life() == 0:
            print("Fail! - " + self.guess.secretWord)
            self.gameOver = True
            # 메시지 ("Fail!" + 비밀 단어) 출력하고, self.gameOver 는 True 로


if __name__ == '__main__':
    import sys
    game = HangmanGame()
