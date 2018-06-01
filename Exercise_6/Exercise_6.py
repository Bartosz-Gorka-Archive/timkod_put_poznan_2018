import math
import operator
from bitarray import bitarray


def read_file(file_name, permissions='r'):
    file = open(file_name, permissions)
    return file.read()


def analyze_content(content):
    dictionary = {}
    for char in content:
        cardinality = dictionary.get(char, 0)
        dictionary.update({char: cardinality + 1})

    return dictionary


def sort_dictionary_items(dictionary):
    return dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True))


def int2bits(i, fill=8):
    return bin(i)[2:].zfill(fill)


class BasicLZW:
    def __init__(self, content, characters):
        self.content = content
        self.characters_dictionary = characters

    def create(self):
        dictionary_with_codes = {}
        for index, key in enumerate(self.characters_dictionary.keys()):
            dictionary_with_codes.update({key: index + 1})

        return dictionary_with_codes

    @staticmethod
    def codes_to_bits(codes):
        dict_with_bits_codes = {}
        total_items = len(codes)
        fill = int(math.log(total_items, 2) + 1)
        for (char, code) in codes.items():
            bits = int2bits(code, fill=fill)
            dict_with_bits_codes.update({char: bitarray(bits).to01()})

        return dict_with_bits_codes


def main():
    file_name = '../Exercise_3/short_sample.txt'

    ################################
    ####### Lempel–Ziv–Welch #######
    ################################
    content = read_file(file_name, permissions='r')
    characters_dictionary = analyze_content(content)
    sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    basic_lzw = BasicLZW(content, sorted_characters_dictionary)
    lzw_basic_code = basic_lzw.create()
    bits_codes = basic_lzw.codes_to_bits(lzw_basic_code)
    print(bits_codes)


if __name__ == '__main__':
    main()
