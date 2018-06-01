import operator


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


def main():
    file_name = '../Exercise_3/short_sample.txt'

    ################################
    ####### Lempel–Ziv–Welch #######
    ################################
    content = read_file(file_name, permissions='r')
    characters_dictionary = analyze_content(content)
    sorted_characters_dictionary = sort_dictionary_items(characters_dictionary)
    print(sorted_characters_dictionary)


if __name__ == '__main__':
    main()
