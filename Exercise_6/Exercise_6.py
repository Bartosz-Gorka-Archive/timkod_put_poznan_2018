import os
import cv2
import operator
from bitarray import bitarray


def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()


def read_binary_file(file_name):
    content = ''
    with open(file_name, 'rb') as file:
        temp = list(file.read())
        content = ''.join([chr(x) for x in temp])
    return content


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
        fill = total_items.bit_length()
        for (char, code) in codes.items():
            bits = int2bits(code, fill=fill)
            dict_with_bits_codes.update({char: bits})

        return dict_with_bits_codes

    def encode(self, codes):
        code = []
        current_key = ''
        basic_key = ''
        last_element_num = len(codes)
        current_bit_length = last_element_num.bit_length()

        for letter in self.content:
            current_key += letter
            if current_key in codes:
                basic_key += letter
            else:
                code.append(codes.get(basic_key))
                last_element_num += 1

                # Bump bits array - max length used
                if last_element_num.bit_length() > current_bit_length:
                    current_bit_length += 1
                    for key, value in codes.items():
                        codes.update({key: '0' + value})

                # Update dictionary
                codes.update({current_key: str(int2bits(last_element_num, fill=current_bit_length))})
                basic_key = letter
                current_key = letter

        code.append(codes.get(basic_key))
        return code

    @staticmethod
    def decode(codes, encoded_content):
        content = []
        last_key = ''
        index = 0
        last_element_num = len(codes)
        current_bit_length = last_element_num.bit_length()
        max_index = len(encoded_content)

        while True:
            bits_code = encoded_content[index:index + current_bit_length].to01()
            index += current_bit_length
            char = codes.get(bits_code)

            if char is not None:
                last_element_num += 1
                codes.update({int2bits(last_element_num, fill=current_bit_length): char})

                if last_key != '':
                    last_key += char[0]
                    codes.update({int2bits((last_element_num - 1), fill=current_bit_length): last_key})

                    if last_element_num.bit_length() > current_bit_length:
                        current_bit_length += 1
                        temp = {}
                        for key, value in codes.items():
                            temp.update({'0' + key: value})
                        codes = temp

                last_key = char
                content.append(char)

                if index >= max_index:
                    break
            else:
                break

        return ''.join(content)


def load_dictionary(file_name):
    dictionary = {}
    with open(file_name, 'r') as file:
        content = file.read()
        fill = len(content).bit_length()
        for index, char in enumerate(content):
            bits = int2bits(index + 1, fill=fill)
            dictionary.update({bits: char})

    return dictionary


def load_content(file_name):
    content = bitarray()
    with open(file_name, 'rb') as file:
        content.fromfile(file)
    return content


def write_list(encoded_content_list, file_name):
    with open(file_name, 'wb') as file:
        bitarray.tofile(bitarray(''.join(encoded_content_list)), file)


def write_dictionary(dictionary, file_name):
    with open(file_name, 'w') as file:
        for key in dictionary.keys():
            file.write(key)


def calculate_size(file_name):
    return os.stat(file_name).st_size


def main():
    # file_name = '../Exercise_3/short_sample.txt'
    file_name = 'norm_wiki_sample.txt'
    # content = read_binary_file('lena.bmp')

    ################################
    ####### Lempel–Ziv–Welch #######
    ################################
    content = read_file(file_name)
    characters_dictionary = analyze_content(content)
    sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    basic_lzw = BasicLZW(content, sorted_characters_dictionary)
    lzw_basic_code = basic_lzw.create()
    bits_codes = basic_lzw.codes_to_bits(lzw_basic_code)
    write_dictionary(lzw_basic_code, 'lzw_dictionary.txt')

    encoded_content = basic_lzw.encode(bits_codes)
    write_list(encoded_content, 'lzw_content.bin')
    encoded = load_content('lzw_content.bin')
    decode_codes = load_dictionary('lzw_dictionary.txt')
    decoded = basic_lzw.decode(decode_codes, encoded)

    print('LZW basic format')
    print('\tBefore =>', calculate_size(file_name), '[bytes]')
    print('\tAfter  =>', calculate_size('lzw_content.bin'), '[bytes]')


if __name__ == '__main__':
    main()
