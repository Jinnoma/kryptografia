import sys
from abc import ABC, abstractmethod

class CipherError(Exception):
    """Raised when the input value is too large"""
    pass

class Cipher(ABC):

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @abstractmethod
    def cryptanalysis(self):
        pass

    @abstractmethod
    def cryptanalysis_with_plain_text(self):
        pass


class Caesar(Cipher):

    def __init__(self, a):
        self.a = a

    def encrypt(self):
        result = ""
        with open('plain.txt', 'r') as file:
            plain = file.read()
        for p in plain:
            if 96 < ord(p) < 123:
                result += chr((ord(p) + a - 97) % 26 + 97)
            elif ord(p) > 64:
                result += chr((ord(p) + a - 65) % 26 + 65)
            else:
                result += p

        text_file = open('crypto.txt', 'w')
        text_file.write(result)
        text_file.close()

    def decrypt(self):
        result = ""
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        for c in crypto:
            if 96 < ord(c) < 123:
                result += chr((ord(c) - a - 97) % 26 + 97)
            elif ord(c) > 64:
                result += chr((ord(c) - a - 65) % 26 + 65)
            else:
                result += c

        text_file = open('decrypt.txt', 'w')
        text_file.write(result)
        text_file.close()

    def cryptanalysis(self):
        result = ""

        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        for i in range(1, 26):
            for c in crypto:
                if 96 < ord(c) < 123:
                    result += chr((ord(c) - i - 97) % 26 + 97)
                elif ord(c) > 64:
                    result += chr((ord(c) - i - 65) % 26 + 65)
                else:
                    result += c

            text_file = open('decrypt.txt', 'w')
            text_file.write(result)
            text_file.close()

    def cryptanalysis_with_plain_text(self):

        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        with open('extra.txt', 'r') as file:
            extra = file.read()

        for i in range(1, 26):
            result = ''
            for c in crypto:
                if 96 < ord(c) < 123:
                    result += chr((ord(c) - i - 97) % 26 + 97)
                elif ord(c) > 64:
                    result += chr((ord(c) - i - 65) % 26 + 65)
                else:
                    result += c

            if extra in result:
                key = str(i)
                text_file = open('decrypt.txt', 'w')
                text_file.write(result)
                text_file.close()
                text_file1 = open('key-new.txt','w')
                text_file1.write(key)
                text_file1.close()
                return True


class Affine(Cipher):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def modular_inverse(a):
        for i in range(1, 27):
            if (a * i) % 26 == 1:
                return i

    def encrypt(self):
        result = ""
        with open('plain.txt', 'r') as file:
            crypto = file.read()

        for c in crypto:
            if 96 < ord(c) < 123:
                result += chr((a * (ord(c) - 97) + b) % 26 + 97)
            elif ord(c) > 64:
                result += chr((a * (ord(c) - 65) + b) % 26 + 65)
            else:
               result += c

        text_file = open('crypto.txt', 'w')
        text_file.write(result)
        text_file.close()

    def decrypt(self):
        result = ""
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        try:
            mod_inv = self.modular_inverse(a)
            if mod_inv == None:
                raise CipherError
        except CipherError:
            print('Invalid key')
            return False

        for c in crypto:
            if 96 < ord(c) < 123:
                result += chr((mod_inv * (ord(c) - 97 - b)) % 26 + 97)
            elif ord(c) > 64:
                result += chr((mod_inv * (ord(c) - b - 65)) % 26 + 65)
            else:
                result += c

        text_file = open('decrypt.txt', 'w')
        text_file.write(result)
        text_file.close()

    def cryptanalysis(self):
        result = ""
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

            for i in range(1,27):
                for j in range(1,27):
                    mod_inv = self.modular_inverse(j)
                    if mod_inv != None:
                        for c in crypto:
                            if 96 < ord(c) < 123:
                                result += chr((mod_inv * (ord(c) - 97 - i)) % 26 + 97)
                            elif ord(c) > 64:
                                result += chr((mod_inv * (ord(c) - i - 65)) % 26 + 65)
                            else:
                                result += c

                            text_file = open('decrypt.txt', 'w')
                            text_file.write(result)
                            text_file.close()

    def cryptanalysis_with_plain_text(self):
        result = ""
        with open('crypto.txt', 'r') as file:
            crypto = file.read()

        with open('extra.txt','r') as file:
            extra = file.read()

            for i in range(1,27):
                for j in range(1,27):
                    result = ''
                    mod_inv = self.modular_inverse(j)
                    if mod_inv != None:
                        for c in crypto:
                            if 96 < ord(c) < 123:
                                result += chr((mod_inv * (ord(c) - 97 - i)) % 26 + 97)
                            elif ord(c) > 64:
                                result += chr((mod_inv * (ord(c) - i - 65)) % 26 + 65)
                            else:
                                result += c

                    if extra in result:
                        keys = f'{j} {i} '
                        text_file = open('key-new.txt', 'w')
                        text_file.write(keys)
                        text_file.close()
                        text_file = open('decrypt.txt', 'w')
                        text_file.write(result)
                        text_file.close()
                        return True
        print("Can't find key")




if __name__ == '__main__':
    with open('key.txt', 'r') as file:
        keys = file.read()
    keys = keys.split()

    try:
        a = int(keys[0])
        b = int(keys[1])
    except ValueError:
        print('Invalid key')

    if sys.argv[1] == '-c':
        cipher = Caesar(a)
    elif sys.argv[1] == '-a':
        cipher = Affine(a,b)
    if sys.argv[2] == '-e':
        cipher.encrypt()
    elif sys.argv[2] == '-d':
        cipher.decrypt()
    elif sys.argv[2] == '-k':
        cipher.cryptanalysis()
    elif sys.argv[2] == '-j':
        cipher.cryptanalysis_with_plain_text()

