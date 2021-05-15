# Author: Przemysław Guzek
import sys
from random import randint
from math import gcd
import binascii


class Elgamal:

    @staticmethod
    def encrypt():
        with open('public.txt', 'r') as f:
            lines = f.read().splitlines()
            p, g, pub_b = map(int, lines)

        with open('plain.txt', 'r') as f:
            m = f.read()

        m = Elgamal.to_bytes(m)

        if m >= p:
            raise ValueError('Too long message.')

        with open('crypto.txt', 'w') as f:
            k = randint(0, p - 1)
            r = pow(g, k, p)
            t = pow(pub_b, k, p) * m
            f.write(str(r) + ' ' + str(t) + '\n')

    @staticmethod
    def decrypt():
        with open('crypto.txt') as f:
            cipher = f.read().splitlines()[0]

        with open('private.txt') as f:
            lines = f.read().splitlines()
            p, _, priv_b = map(int, lines)

        with open('decrypt.txt', 'w') as f:
            r, t = map(int, cipher.split())
            letter = t // pow(r, priv_b, p)
            l = (Elgamal.to_string(letter))
            f.write(str(l.decode('utf-8')))

    def to_bytes(str):
        return int(binascii.hexlify(str.encode()), 16)

    def to_string(bytes):
        return binascii.unhexlify('%x' % bytes)

    @staticmethod
    def keys():
        with open('elgamal.txt', 'r') as f:
            lines = f.read().splitlines()
            p, g = map(int, lines)

        private = randint(1, p - 2)
        publ = pow(g, private, p)

        with open('private.txt', 'w') as f:
            f.write('%d\n%d\n%d' % (p, g, private))

        with open('public.txt', 'w') as f:
            f.write('%d\n%d\n%d' % (p, g, publ))


    @staticmethod
    def signature():
        with open('private.txt', 'r') as f:
            lines = f.read().splitlines()
            p, g, priv_b = map(int, lines)

        with open('message.txt', 'r') as f:
            message = f.read()
            m = Elgamal.to_bytes(message)

        while True:
            k = randint(1, p - 2)
            if gcd(k, p - 1) == 1:
                break

        if m >= p:
            raise ValueError('Too long message.')

        r = pow(g, k, p)
        l = pow(k, -1, p - 1)
        x = l * (m - priv_b * r) % (p - 1)

        with open('signature.txt', 'w') as f:
            f.write(str(r) + '\n' + str(x))

    @staticmethod
    def verify():
        with open('message.txt', 'r') as f:
            message = f.read()
            m = Elgamal.to_bytes(message)

        with open('signature.txt', 'r') as f:
            lines = f.read().splitlines()
            rr, xx = map(int, lines)

        with open('public.txt', 'r') as f:
            lines = f.read().splitlines()
            p, g, pub_b = map(int, lines)

        if rr < 1 or rr > p - 1:
            print('N')
            verify = 'N'

        v1 = pow(pub_b, rr, p) % p * pow(rr, xx, p) % p
        v2 = pow(g, m, p)

        if v1 == v2:
            print('T')
            verify = 'T'
        else:
            print('N')
            verify = 'N'

        with open('verify.txt', 'w') as f:
            f.write(verify)


if __name__ == "__main__":

    if sys.argv[1] == '-k':
        Elgamal.keys()
    elif sys.argv[1] == '-e':
        Elgamal.encrypt()
    elif sys.argv[1] == '-d':
        Elgamal.decrypt()
    elif sys.argv[1] == '-s':
        Elgamal.signature()
    elif sys.argv[1] == '-v':
        Elgamal.verify()
