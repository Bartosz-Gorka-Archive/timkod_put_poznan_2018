import heapq
import operator
from bitarray import bitarray


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

    return bitarray(''.join(code))


# Main function
def main():
    file_name = '../Exercise_3/short_sample.txt'

    content = read_file(file_name)
    letters_dictionary, counter = analyze_content(content)
    ordered_dictionary = order_dictionary(letters_dictionary)
    code = create(ordered_dictionary)
    encoded = encode(code, content)


if __name__ == '__main__':
    main()
