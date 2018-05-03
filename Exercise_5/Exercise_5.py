import operator


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
    return sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)


# Main function
def main():
    file_name = '../Exercise_3/short_sample.txt'

    content = read_file(file_name)
    letters_dictionary, counter = analyze_content(content)
    ordered_dictionary = order_dictionary(letters_dictionary)


if __name__ == '__main__':
    main()
