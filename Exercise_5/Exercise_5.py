import os
import math
import heapq
import operator
from bitarray import bitarray


END_CONTENT_CHAR = '$'


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.freq


# Read file - return content
def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()


# Analyze content - calculate probability
def analyze_content(content):
    letters = {}
    counter = 0

    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    return letters, counter


# Order letters dictionary - top used as first
def order_dictionary(dictionary):
    return dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True))


# Make heap of nodes
def make_nodes_heap(dictionary):
    heap = []
    for (key, value) in dictionary.items():
        node = Node(key, value)
        heapq.heappush(heap, node)
    return heap


# Merge nodes to prepare binary tree
def merge_nodes(heap):
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)
    return heap


# Code helper to prepare dictionary with codes and characters
def code_helper(root, current_code, codes):
    # Return when None
    if not root:
        return

    # Required assign character to node (only leaf has)
    if root.char:
        codes[root.char] = current_code
        return

    # Recursion
    code_helper(root.left, current_code + '0', codes)
    code_helper(root.right, current_code + '1', codes)


# Prepare codes
def make_codes(heap):
    current_code = ''
    codes = {}
    root = heapq.heappop(heap)

    code_helper(root, current_code, codes)
    return codes


# Create code
def create(dictionary):
    nodes = make_nodes_heap(dictionary)
    heap = merge_nodes(nodes)
    codes = make_codes(heap)
    return codes


# Encode text
def encode(code_dict, text):
    code = []
    for letter in text:
        code.append(code_dict.get(letter))

    # Append end of stream
    code.append(code_dict.get(END_CONTENT_CHAR))
    return bitarray(''.join(code))


# Simple cast char to bits
def string2bits(s):
    return [bin(ord(x))[2:].zfill(8) for x in s]


# Save encoded details to file
def save(code_dict, encoded_content, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + 'encoded_result.bin', 'wb') as content_file:
        encoded_content.tofile(content_file)
    with open(directory + 'key.bin', 'wb') as key_file:
        code_bits = []
        for (key, value) in code_dict.items():
            for x in string2bits(key):
                code_bits.append(x)
            for x in string2bits(str(len(value))):
                code_bits.append(x)
            for x in string2bits(':'):
                code_bits.append(x)
            code_bits.append(value)
        key_file.write(bitarray(''.join(code_bits)).tobytes())


# Load content from file
def load(directory):
    encoded_content = bitarray()
    encoded_key = bitarray()
    code = {}

    with open(directory + 'encoded_result.bin', 'rb') as content_file:
        encoded_content.fromfile(content_file)

    with open(directory + 'key.bin', 'rb') as key_file:
        encoded_key.fromfile(key_file)

    total_length = encoded_key.length()
    length = 0
    while length < total_length:
        key = encoded_key[length: length + 8].tostring()
        length += 8
        size = []
        temp = '0'
        while temp != ':' and temp != '':
            size.append(temp)
            temp = encoded_key[length: length + 8].tostring()
            length += 8

        code_length = int(''.join(size))
        code_bits = encoded_key[length: length + code_length].to01()
        length += code_length
        code[code_bits] = key

    return encoded_content, code


# Decode already encoded text
def decode(encoded_bits, code_dict):
    decoded = ''
    current_code = ''

    for bit in encoded_bits.to01():
        current_code += str(bit)
        if current_code in code_dict:
            char = code_dict.get(current_code)
            if char != END_CONTENT_CHAR:
                decoded += char
                current_code = ''
            else:
                return decoded

    return decoded


# Calculate size
def calculate_sizes(directory, original):
    encoded_size = os.stat(directory + 'encoded_result.bin').st_size
    key_size = os.stat(directory + 'key.bin').st_size
    original_size = os.stat(original).st_size
    return encoded_size, key_size, original_size


def entropy(dictionary):
    # Entropy sum
    entropy_result = 0.0

    # Loop to analyze
    for key, value in dictionary.items():
        entropy_result += value * math.log(value, 2)

    # Return result
    return -entropy_result


def to_probability(dictionary, counter):
    for letter in dictionary:
        dictionary.update({letter: dictionary.get(letter) / counter})
    return dictionary


# Main function
def main():
    directory = 'encoded/'
    file_name = 'norm_wiki_sample.txt'

    content = read_file(file_name)
    letters_dictionary, counter = analyze_content(content)
    counter += 1
    letters_dictionary.update({END_CONTENT_CHAR: 1})
    ordered_dictionary = order_dictionary(letters_dictionary)
    code = create(ordered_dictionary)
    encoded = encode(code, content)
    save(code, encoded, directory)
    encoded_content, enc_code = load(directory)
    decoded = decode(encoded_content, enc_code)

    en_size, k_size, o_size = calculate_sizes(directory, file_name)
    sum_size = k_size + en_size
    sd = encoded.length() / len(content)
    ce = entropy(to_probability(letters_dictionary, counter)) / sd

    print('Original file => ' + file_name)
    print('Size          => ' + str(o_size) + ' [bytes]')

    print('Encoded size:')
    print('\tEncoded   => ' + str(en_size) + ' [bytes]')
    print('\tKey       => ' + str(k_size) + ' [bytes]')
    print('\tSUM       => ' + str(sum_size) + ' [bytes]')
    print('\tSD        => ' + str(sd))
    print('\tCE        => ' + str(ce))

    print('Compare files')
    if decoded == content:
        print('\tEquality correct ✓')
        print('\tCompression Ratio => ' + str(o_size / sum_size))
        print('\tSpace savings     => ' + str(1 - sum_size / o_size))
    else:
        print('\tContent =/= Decoded(Encoded(Content))')

        print(content)
        print('\n\n--------\n\n')
        print(decoded)


if __name__ == '__main__':
    main()
