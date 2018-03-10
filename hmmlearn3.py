import sys


class HmmLearn:

    def __init__(self, file_path):
        """
        :param file_path: The file from which the corpus has to be read
        """

        # Define the dictionary keys
        start = '$@#$START$@#$'
        n_tag = 'next'
        count = 'count'
        label = 'label'
        stop = '$@#$STOP$@#$'

        # Initialize both the dictionaries
        tag_dict = dict()
        word_dict = dict()

        # Each tag or word information object
        def element_initalize():
            return {
                n_tag: dict({}),
                count: 1,
                label: dict()
            }

        # Initialize the start tag
        tag_dict[start] = element_initalize()
        tag_dict[start][count] -= 1

        for sentence in open(file_path, encoding='utf8'):
            # Split up the sentence into words
            words = (sentence + ' ' + stop + '/' + stop).split()

            # Start label can only have start word so both of them will have the same count
            tag_dict[start][count] += 1

            # Set the previous state to the start label
            prev_label = start

            # Iterate over the words
            for word in words:
                # Split into words and tags
                word = word.rsplit('/', 1)

                # Check if this word exists in the word dict
                if word_dict.get(word[0]) is None:
                    word_dict[word[0]] = element_initalize()

                    # Set the count of the newly found word's label to 1
                    word_dict[word[0]][label][word[1]] = 1
                else:
                    # Increase the count of the word
                    word_dict[word[0]][count] += 1

                    # Is it a new label and modify its count
                    if word_dict[word[0]][label].get(word[1]) is None:
                        word_dict[word[0]][label][word[1]] = 1
                    else:
                        word_dict[word[0]][label][word[1]] += 1

                # Check if this tag exists in the tag dict
                if tag_dict.get(word[1]) is None:
                    tag_dict[word[1]] = element_initalize()

                    # Set the count of the label's word to 1
                    tag_dict[word[1]][label][word[0]] = 1
                else:
                    tag_dict[word[1]][count] += 1

                    # New word for the label and modify the count of the word
                    if tag_dict[word[1]][label].get(word[0]) is None:
                        tag_dict[word[1]][label][word[0]] = 1
                    else:
                        tag_dict[word[1]][label][word[0]] += 1

                if tag_dict[prev_label][n_tag].get(word[1]) is None:
                    tag_dict[prev_label][n_tag][word[1]] = 1
                else:
                    tag_dict[prev_label][n_tag][word[1]] += 1

                prev_label = word[1]

        content = dict({
            'tags': tag_dict,
            'words': word_dict
        })

        file = open('hmmmodel.txt', 'w', encoding='utf8')
        file.write(str(content))
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Insufficient number of arguments')
        exit(1)
    else:
        hmm = HmmLearn(sys.argv[1])

