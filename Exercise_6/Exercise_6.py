import os
import cv2
import heapq
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


class LZWHuffman:
    def __init__(self, content, characters):
        self.content = content
        self.characters_dictionary = characters

    def create(self):
        dictionary_with_codes = {}
        for index, key in enumerate(self.characters_dictionary.keys()):
            dictionary_with_codes.update({key: index + 1})

        return dictionary_with_codes

    @staticmethod
    def append_counters(codes):
        for key, value in codes.items():
            codes.update({key: [value, 0]})
        return codes

    @staticmethod
    def codes_to_bits(codes):
        dict_with_bits_codes = {}
        total_items = len(codes)
        fill = total_items.bit_length()
        for (char, code) in codes.items():
            bits = int2bits(code, fill=fill)
            dict_with_bits_codes.update({char: bits})

        return dict_with_bits_codes

    def pre_encode(self, codes):
        current_key = ''
        basic_key = ''
        counter = 0
        last_element_num = len(codes)
        current_bit_length = last_element_num.bit_length()

        for letter in self.content:
            current_key += letter
            if current_key in codes:
                basic_key += letter
            else:
                [ind, card] = codes.get(basic_key)
                codes.update({basic_key: [ind, card + 1]})
                last_element_num += 1
                counter += 1

                # Bump bits array - max length used
                if last_element_num.bit_length() > current_bit_length:
                    current_bit_length += 1
                    for key, value in codes.items():
                        [ind, card] = value
                        codes.update({key: ['0' + ind, card]})

                # Update dictionary
                codes.update({current_key: [str(int2bits(last_element_num, fill=current_bit_length)), 0]})
                basic_key = letter
                current_key = letter

        [ind, card] = codes.get(basic_key)
        codes.update({basic_key: [ind, card+1]})
        counter += 1
        return codes, counter

    @staticmethod
    def remove_zero_cardinality_items(codes):
        temp = {}
        for key, item in codes.items():
            [code, cardinality] = item
            if cardinality > 0:
                temp.update({key: [code, cardinality]})
        return temp

    @staticmethod
    def make_nodes_heap(dictionary):
        heap = []
        for key, value in dictionary.items():
            [_bits, cardinality] = value
            node = Node(key, cardinality)
            heapq.heappush(heap, node)
        return heap

    @staticmethod
    def merge_nodes(heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(heap, merged)
        return heap

    def code_helper(self, root, current_code, codes):
        # Return when None
        if not root:
            return

        # Required assign character to node (only leaf has)
        if root.char:
            codes[root.char] = current_code
            return

        # Recursion
        self.code_helper(root.left, current_code + '0', codes)
        self.code_helper(root.right, current_code + '1', codes)

    def make_codes(self, heap):
        current_code = ''
        codes = {}
        root = heapq.heappop(heap)

        self.code_helper(root, current_code, codes)
        return codes

    def huffman_codes(self, dictionary):
        nodes = self.make_nodes_heap(dictionary)
        heap = self.merge_nodes(nodes)
        codes = self.make_codes(heap)
        return codes

    def encode(self, dictionary):
        code = []
        current_key = ''
        basic_key = ''

        for letter in self.content:
            current_key += letter
            if current_key in dictionary:
                basic_key += letter
            else:
                code.append(dictionary.get(basic_key))
                basic_key = letter
                current_key = letter

        code.append(dictionary.get(basic_key))
        return code


class Node:
    def __init__(self, char, card):
        self.char = char
        self.freq = card
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.freq


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
    file_name = '../Exercise_3/short_sample.txt'
    # file_name = 'norm_wiki_sample.txt'
    # content = read_binary_file('lena.bmp')

    ################################
    ####### Lempel–Ziv–Welch #######
    ################################
    # content = read_file(file_name)
    # characters_dictionary = analyze_content(content)
    # sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    # basic_lzw = BasicLZW(content, sorted_characters_dictionary)
    # lzw_basic_code = basic_lzw.create()
    # bits_codes = basic_lzw.codes_to_bits(lzw_basic_code)
    # write_dictionary(lzw_basic_code, 'lzw_dictionary.txt')
    #
    # encoded_content = basic_lzw.encode(bits_codes)
    # write_list(encoded_content, 'lzw_content.bin')
    # encoded = load_content('lzw_content.bin')
    # decode_codes = load_dictionary('lzw_dictionary.txt')
    # decoded = basic_lzw.decode(decode_codes, encoded)
    #
    # print('LZW basic format')
    # print('\tBefore =>', calculate_size(file_name), '[bytes]')
    # print('\tAfter  =>', calculate_size('lzw_content.bin'), '[bytes]')

    #############################
    ####### LZW + Huffman #######
    #############################
    content = read_file(file_name)
    characters_dictionary = analyze_content(content)
    sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    lzw_huffman = LZWHuffman(content, sorted_characters_dictionary)
    lzw_basic_code = lzw_huffman.create()
    bits_codes = lzw_huffman.codes_to_bits(lzw_basic_code)
    codes_with_counters = lzw_huffman.append_counters(bits_codes)
    codes_with_cardinality, total_counter = lzw_huffman.pre_encode(codes_with_counters)
    codes_clear_cardinality = lzw_huffman.remove_zero_cardinality_items(codes_with_cardinality)
    huffman_codes = lzw_huffman.huffman_codes(codes_clear_cardinality)
    encoded = lzw_huffman.encode(huffman_codes)
    print(encoded)


if __name__ == '__main__':
    main()
