# Author: Przemysław Guzek

import numpy as nmp
from PIL import Image as img
from random import randint


class BlockCipher:

    def __init__(self, key):
        self.key = key

    @staticmethod
    def get_divi(div):
        div_list = []
        width = len(div[0])
        div_range = range(2, width + 1)
        list_width = [i for i in div_range if width % i == 0]
        if len(list_width) > 1:
            div_list.append(list_width[1])
        else:
            div_list.append(list_width[0])
        height = len(div)
        div_range = range(2, height + 1)
        list_height = [i for i in div_range if height % i == 0]
        if len(list_width) > 1:
            div_list.append(list_height[1])
        else:
            div_list.append(list_height[0])
        return div_list

    @staticmethod
    def black_and_white(arr):
        black_and_white_list = []
        for a in arr:
            temp = []
            for y in a:
                if nmp.all(nmp.array([y, [255, 255, 255]])):
                    temp.append([1])
                else:
                    temp.append([0])
            black_and_white_list.append(temp)
        return black_and_white_list

    @staticmethod
    def black_and_white_to_arr(black_and_white):
        arr = []
        for x in black_and_white:
            temp = []
            for y in x:
                if nmp.all(nmp.array([y, [1]])):  # white
                    temp.append([255, 255, 255])
                else:  # black
                    temp.append([0, 0, 0])
            arr.append(temp)
        return arr

    @staticmethod
    def black_and_white_to_block(arr, width, height, black_and_white):
        block = []

        for _ in range(len(arr) // height):
            block.append([])

        for i, _ in enumerate(block):
            for _ in range(len(arr[0]) // width):
                block[i].append([])

        counter = 0

        for l, line in enumerate(black_and_white):
            if l % height == 0 and l > 0:
                counter += 1
            count = 0
            for p, px in enumerate(line):
                if p % width == 0 and p > 0:
                    count += 1
                block[counter][count].append(px)
        return block

    @staticmethod
    def block_to_black_and_white(arr, width, height, black_and_white):
        counter = 0
        for l, line in enumerate(black_and_white):
            if l % height == 0 and l > 0:
                counter += 1
            count = 0
            for y, pixel in enumerate(line):
                if y % width == 0 and y > 0:
                    count += 1
                black_and_white[l][y] = arr[counter][
                    count].pop(0)
        return black_and_white

    @staticmethod
    def ECB(key, block_array):
        key_index = 0
        for l, line in enumerate(block_array):
            for y, block in enumerate(line):
                for i, element in enumerate(block):
                    block_array[l][y][i] = [block[i][0] ^ key[key_index % 32][0]]
                    key_index += 1
        return block_array

    @staticmethod
    def CBC(key, arr, width, height):
        key_index = 0
        block1 = []
        for x in range(height * width):
            block1.append([randint(0, 1)])
        for x, line in enumerate(arr):
            for y, block in enumerate(line):
                temp = []
                for k in range(len(block)):
                    temp.append([block1[k][0] ^ block[k][0]])
                arr[x][y] = temp
                for i, element in enumerate(block):
                    arr[x][y][i] = [
                        arr[x][y][i][0] ^ key[key_index % 32][0]]
                    key_index += 1
                block1 = arr[x][y]
        return arr

    def encrypt(self):
        image = img.open("plain.bmp")
        arr = nmp.asarray(image)
        width, height = BlockCipher.get_divi(arr)
        arr_bw = BlockCipher.black_and_white(arr)
        block_array = BlockCipher.black_and_white_to_block(arr, width, height, arr_bw)
        ecb_array = BlockCipher.ECB(self.key, block_array)
        arr_ecb = BlockCipher.block_to_black_and_white(ecb_array, width, height, arr_bw)
        ecb = BlockCipher.black_and_white_to_arr(arr_ecb)

        arr_bw = BlockCipher.black_and_white(arr)
        block_array = BlockCipher.black_and_white_to_block(arr, width, height, arr_bw)
        cbc_array = BlockCipher.CBC(self.key, block_array, width, height)
        arr_cbc = BlockCipher.block_to_black_and_white(cbc_array, width, height, arr_bw)
        cbc = BlockCipher.black_and_white_to_arr(arr_cbc)

        return nmp.array(cbc), nmp.array(ecb)


if __name__ == '__main__':

    key = []
    for x in range(32):
        key.append([randint(0, 1)])

    cbc, ecb = BlockCipher(key).encrypt()
    cbc = img.fromarray(cbc.astype(nmp.uint8))
    ecb = img.fromarray(ecb.astype(nmp.uint8))
    cbc.save("cbc_crypto.bmp")
    ecb.save("ecb_crypto.bmp")
