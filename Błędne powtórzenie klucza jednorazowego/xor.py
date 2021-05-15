import sys

class Xor():

    @staticmethod
    def encrypt():
        text = open("plain.txt", "r").readlines()
        for x in range(len(text)):
            if "\n" in text[x]:
                text[x] = text[x][:-1]
        encrypted = []
        key = open("key.txt", "r").read()
        new_key = ""
        for x in range(32):
            new_key += key[x % len(key)]
        for l in text:
            temp = []
            for i, _char in enumerate(l):
                temp.append(Xor.xor(_char, new_key[i]))
            encrypted.append(temp)
        to_file = ""
        for line in encrypted:
            for _char in line:
                to_file += _char
        byte_to_file = to_file.encode("utf8")
        open("crypto.txt", "wb").write(byte_to_file)

    @staticmethod
    def crypto():
        text = open("crypto.txt", "rb").read()
        key = []
        for x in range(32):
            key.append("")
        for i, _char in enumerate(text):
            if format(_char, '08b').startswith("010"):
                if key[i % 32] == "":
                    key[i % 32] = Xor.xor(" ", chr(_char))
        return_key = ""
        decrypted = ""
        for x in key:
            if x != "":
                return_key += x
            else:
                return_key += "a"
        for i, _char in enumerate(text.decode("utf8")):
            if i % 32 == 0 and i != 0:
                decrypted += "\n"
            decrypted += Xor.xor(_char, return_key[i % len(return_key)])
        open("decrypt.txt", "w").write(decrypted)

    @staticmethod
    def prepare():
        with open('orig.txt', 'r') as file:
            orig = file.read()
        prepared = ""
        for i, _char in enumerate(orig):
            forbidden = """~“”\,.!?:;*'%/|"‘+-=()[]{}’-0123456789<>@"""
            if (_char not in forbidden) and _char != "\n":
                if i > 0:
                    if not (prepared[-1] == " " and orig[i] == " "):
                        prepared += _char.lower()
                else:
                    prepared += _char.lower()
            elif _char == "\n":
                if i > 0:
                    if prepared[-1] != " ":
                        prepared += " "
        new_text = ""
        for i, _char in enumerate(prepared):
            i += 1

            if i % 32 == 0 and i != 0:
                new_text += _char
                new_text += "\n"
            else:
                new_text += _char
        text_file = open('plain.txt', 'w')
        text_file.write(new_text)
        text_file.close()

    def xor(s1, s2):
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


if __name__ == '__main__':
    if sys.argv[1] == '-p':
        Xor.prepare()
    elif sys.argv[1] == '-e':
        Xor.encrypt()
    elif sys.argv[1] == '-k':
        Xor.crypto()