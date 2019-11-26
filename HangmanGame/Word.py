import random


class Word:
    def __init__(self, filename):
        self.__words = []
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()

        self.__words_size = 0
        for line in lines:
            word = line.rstrip()
            self.__words.append(word)
            self.__words_size += 1

        print("%d words in DB" % self.__words_size)

    def test(self):
        return 'default'

    def randFromDB(self, min_length, max_length):
        filtered_words = []
        for word in self.__words:
            if min_length <= len(word) <= max_length:
                filtered_words += [word]

        if len(filtered_words) == 0:
            return None
        # r = random.randrange(self.__words_size)
        r = random.randrange(len(filtered_words))
        # return self.__words[r]
        return filtered_words[r]
