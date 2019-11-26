import HangmanGame.AsciiArt


class Hangman:
    def __init__(self):
        self.__state_picture = HangmanGame.AsciiArt.hangman_ascii_art[::-1]
        self.__life = len(self.__state_picture) - 1

    def life_decrease(self):
        self.__life -= 1
        if self.__life < 0:
            raise

    def is_dead(self):
        return self.__life == 0

    def get_life(self):
        return self.__life

    def current_shape(self):
        return self.__state_picture[self.__life]


if __name__ == "__main__":
    hangman = Hangman()
    while hangman.get_life():
        hangman.life_decrease()
        print(hangman.get_life())
        print(hangman.is_dead())
