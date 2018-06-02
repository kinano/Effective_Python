import argparse
import collections

def get_file_words(filePath):
    """
    @param filePath str
    @return generator
    """
    with open(filePath, 'r') as file:
        for line in file:
            for word in line.split():
                yield word

def process_word(word, term_container):
    """
    @param filePath str
    @param container
    """
    term_container[word] += 1

if __name__ == "__main__":
    # Define the expected arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        help='Source text file',
        type=str,
        required=True
    )

    # Parse the arguments
    args = parser.parse_args()
    filePath = args.i

    # Initialize the data structure
    term_container = collections.defaultdict(int)

    # Iterate through the word generator
    for word in get_file_words(filePath):
        process_word(
            word=word,
            term_container=term_container
        )

    print term_container

