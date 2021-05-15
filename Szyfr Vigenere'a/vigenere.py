import collections
import string
import sys, re
from collections import Counter

class Vigenere:

    @staticmethod
    def prepare():
        with open('orig.txt', 'r') as file:
            orig = file.read()
        plain = re.sub('[^A-Za-z]+', '', orig).lower()
        text_file = open('plain.txt', 'w')
        text_file.write(plain)
        text_file.close()

    @staticmethod
    def crypto():
        crypto = ''
        with open('plain.txt', 'r') as file:
            plain = file.read()
        with open('key.txt', 'r') as file:
            key = list(file.read())

            for i in range(len(plain) -
                           len(key)):
                key.append(key[i % len(key)])

            for i in range(len(plain)):
                x = (ord(plain[i]) + ord(key[i]) - 97 - 97) % 26 + 97
                crypto += chr(x)
            text_file = open('crypto.txt', 'w')
            text_file.write(crypto)
            text_file.close()

    @staticmethod
    def decrypt():
        decrypt = ''
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        with open('key.txt', 'r') as file:
            key = list(file.read())

        for i in range(len(crypto) - len(key)):
            key.append(key[i % len(key)])

        print(len(key))
        print(len(crypto))

        for i in range(len(crypto)):
            x = (ord(crypto[i]) - ord(key[i])) % 26 + 97
            decrypt += chr(x)
        text_file = open('decrypt.txt', 'w')
        text_file.write(decrypt)
        text_file.close()

    @staticmethod
    def cryptoanalisis():
        password = ''
        english_frequences = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
                              0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                              0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                              0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
        s = '.'
        ic = 0.066
        key = []
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        for i in range(50):
            matches = 0
            for j in range(len(crypto)):
                shift = s + crypto
                if crypto[j] == shift[j]:
                    matches += 1
            key.append(matches / len(crypto))
            s += '.'
        for i in range(4, len(key)):
            if (ic - key[i]) < 0.008:
                password_len = i + 1
                break

        print(password_len)

        alph = list(string.ascii_lowercase)

        for i in range(password_len):
            letters = []

            for j in range(0, len(crypto), password_len):

                try:
                    letters.append(crypto[j + i])
                except IndexError:
                    pass
                counts = Counter(letters)
                occurrence = []
                for k in alph:
                    occurrence.append(counts[k] / sum(counts.values()))

                occurrence = collections.deque(occurrence)
                result = 0
                max = 0
                for l in range(26):
                    o = []

                    for n in range(26):
                        o.append(occurrence[n] * english_frequences[n])
                    if sum(o) > max:
                        max = sum(o)
                        result = l

                    occurrence.rotate(-1)
            password += alph[result]

        text_file = open('key-crypto.txt', 'w')
        text_file.write(password)
        text_file.close()

        key = list(password)
        for i in range(len(crypto) - len(key)):
            key.append(key[i % len(key)])

        decrypt = ''
        for i in range(len(crypto)):
            x = (ord(crypto[i]) - ord(key[i])) % 26 + 97
            decrypt += chr(x)
        text_file = open('decrypt.txt', 'w')
        text_file.write(decrypt)
        text_file.close()


if __name__ == '__main__':

    if sys.argv[1] == '-p':
        Vigenere.prepare()
    elif sys.argv[1] == '-e':
        Vigenere.crypto()
    elif sys.argv[1] == '-d':
        Vigenere.decrypt()
    elif sys.argv[1] == '-k':
        Vigenere.cryptoanalisis()
