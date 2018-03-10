import sys
from math import log10, inf
import time


class HmmDecode:
    def __init__(self, file_path):
        """
        :param file_path: File path where the model is located
        """

        start_time = time.time()

        # Open the model trained
        file = open('hmmmodel.txt', encoding='utf8')

        # Parse the model from string to the dict
        model = file.read()
        model = eval(model)
        tag_dict = model['tags']
        word_dict = model['words']
        file.close()

        # Define the dictionary keys
        start = '$@#$START$@#$'
        n_tag = 'next'
        count = 'count'
        label = 'label'
        stop = '$@#$STOP$@#$'
        prev = 'prev'
        prob = 'log_prob'

        def possible_states_initialize(p, s):
            return {
                prob: p,
                prev: s
            }

        file = open('hmmoutput.txt', 'w', encoding='utf8')

        # Read the file to be labelled
        for sentence in open(file_path, encoding='utf8'):
            # Split up the sentence into words
            words = (sentence + ' ' + stop).split()

            # List of objects of possible states at each location and the previous state probability being 1
            p_states_seq = [{start: possible_states_initialize(log10(1), None)}]

            # Iterate over the words in the sentence
            for word in words:
                # Possible states for this observation
                possible_states = {}

                # Check if the word was registered by the learning algorithm
                if word_dict.get(word) is None:
                    # Emission prob for unknown is 1
                    p_obs = 1
                    possible_tags_list = tag_dict.keys()
                else:
                    # Marks the flag for prob calculation
                    p_obs = 0
                    possible_tags_list = word_dict[word][label].keys()

                # All possible states(tags) for an observation
                for tag in possible_tags_list:
                    # Initialize the probability of the being in that state, aplha
                    possible_states[tag] = possible_states_initialize(-inf, None)

                    # If probability is less than 1 that means it need to be retrieved
                    if p_obs < 1:
                        p_obs = log10(tag_dict[tag][label][word]) - log10(tag_dict[tag][count])

                    prev_states = p_states_seq[len(p_states_seq)-1]
                    # Calculate the overall probability of being at this state
                    for prev_state in prev_states.keys():
                        # Probability calculation prev prob * transition prob * emission prob
                        temp_prob = prev_states[prev_state][prob] + \
                                    log10(1 + tag_dict[prev_state][n_tag].get(tag, 0)) - \
                                    log10(len(tag_dict.keys()) + tag_dict[prev_state][count]) + p_obs

                        # Check for the max prob
                        if temp_prob > possible_states[tag][prob]:
                            possible_states[tag] = possible_states_initialize(temp_prob, prev_state)

                # Append the possible states/tags to the sequence
                p_states_seq.append(possible_states)

            # Start from stop with interesting tag and remove stop from the sequence
            key_interest = p_states_seq[len(p_states_seq)-1][stop][prev]
            p_states_seq.remove(p_states_seq[len(p_states_seq)-1])

            # List of tag sequence generated
            probable_tags = []

            for possible_states in p_states_seq[::-1]:
                probable_tags.insert(0, key_interest)
                key_interest = possible_states[key_interest][prev]

            # Remove the start tag
            probable_tags.pop(0)

            # Track of the number of words written
            c = 1
            for w, t in zip(words, probable_tags):
                file.write(w + "/" + t)
                if c < len(sentence):
                    file.write(" ")
                    c += 1
            # End the file with new line
            file.write("\n")
        file.close()
        print(time.time() - start_time)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Insufficient number of arguments')
        exit(1)
    else:
        hmm = HmmDecode(sys.argv[1])