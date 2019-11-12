import math

romanList = ["I", "V", "X", "L", "C", "D", "M"]
decToRomanList = []


def initDecToRomanList():
    global decToRomanList
    n = len(romanList)
    cnt = [0] * n
    while cnt[n - 1] < 4:
        cnt[0] += 1
        for i in range(n - 1):
            if ((i % 2 == 0 and cnt[i] == 5)
                    or (i % 2 == 1 and cnt[i] == 2)):
                cnt[i + 1] += 1
                cnt[i] = 0
        if cnt[n - 1] == 4:
            break
        str = ""
        for i in reversed(range(n)):
            if (cnt[i] == 4):
                str += romanList[i] + romanList[i + 1]
            else:
                for j in range(cnt[i]):
                    str += romanList[i]
        decToRomanList += [str]

def factorial(num):
    num = int(num)
    if num == 1:
        return 1
    return factorial(num - 1) * num

def decToBin(dec):
    dec = int(dec)
    if dec <= 1:
        return str(dec)
    return decToBin(dec // 2) + str(dec % 2)

def binToDec(bin):
    bin = int(bin)
    if bin == 1:
        return 1
    return binToDec(bin // 10) * 2 + bin % 10

def decToRoman(dec):
    dec = int(dec)
    return decToRomanList[dec - 1]

def romanToDec(roman):
    for i in range(len(decToRomanList)):
        if decToRomanList[i] == roman:
            return i + 1
    return -1



functionList = [
    ('factorial (!)', factorial),
    ('-> binary', decToBin),
    ('binary ->', binToDec),
    ('-> roman', decToRoman),
    ('roman', romanToDec)
]
initDecToRomanList()
if __name__ == "__main__":
    print(decToRoman(876))
    a = decToBin(7)
    print(a)
    print(binToDec(int(a)))
    print(functionList)
    print(decToRomanList)
    print(romanToDec(""))
    #print(functionList[2])