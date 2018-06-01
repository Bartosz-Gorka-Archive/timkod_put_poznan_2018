import cv2
import operator
from bitarray import bitarray


def read_file(file_name):
    file = open(file_name, 'r')
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
        fill = total_items.bit_length()
        for (char, code) in codes.items():
            bits = int2bits(code, fill=fill)
            dict_with_bits_codes.update({char: bitarray(bits).to01()})

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
                        codes.update({key: bitarray('0' + value).to01()})

                # Update dictionary
                codes.update({current_key: bitarray(int2bits(last_element_num, fill=current_bit_length)).to01()})
                basic_key = letter
                current_key = letter

        code.append(codes.get(basic_key))
        return code


def load_dictionary(file_name):
    dictionary = {}
    with open(file_name, 'r') as file:
        content = file.read()
        for index, char in enumerate(content):
            dictionary.update({char: index + 1})

    return dictionary


def write_list(encoded_content_list, file_name):
    with open(file_name, 'wb') as file:
        bitarray.tofile(bitarray(''.join(encoded_content_list)), file)


def write_dictionary(dictionary, file_name):
    with open(file_name, 'w') as file:
        for key in dictionary.keys():
            file.write(key)


def main():
    file_name = '../Exercise_3/short_sample.txt'
    # file_name = 'wiki_sample.txt'

    ################################
    ####### Lempel–Ziv–Welch #######
    ################################
    # lena = 'lena.bmp'
    # file = open(lena, 'rb')
    # test = list(file.read())
    # test_content = ''
    # for i in test[0:100]:
    #     test_content += chr(i)

    # content = read_file(file_name)
    # content = content[0:100]
    # # content = test_content
    # characters_dictionary = analyze_content(content)
    # sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    # basic_lzw = BasicLZW(content, sorted_characters_dictionary)
    # lzw_basic_code = basic_lzw.create()
    # # print(lzw_basic_code)
    # bits_codes = basic_lzw.codes_to_bits(lzw_basic_code)
    # print(bits_codes)
    # write_dictionary(lzw_basic_code, 'lzw_dictionary.txt')
    #
    # encoded_content = basic_lzw.encode(bits_codes)
    # write_list(encoded_content, 'lzw_content.bin')
    # # print(len(test))
    # print(bits_codes)
    # print(encoded_content)
    # print(len(content))
    # print(len(encoded_content))

    lzw = BasicLZW('', {})
    d = load_dictionary('lzw_dictionary.txt')
    print(lzw.codes_to_bits(d))


if __name__ == '__main__':
    main()
