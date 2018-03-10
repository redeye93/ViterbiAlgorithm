# ViterbiAlgorithm
Parts of Speech tagger HMM model based on Viterbi's algorithm. 

The program hmmlearn.py takes in a labelled corpus and generates a model using this training data and saves it in a hmmmodel.txt. This file is later on referred by hmmdecode.py to label the data. The accuracy of this code on the given training corpus is 88.7910423972 on the english language data set and 86.9547119547 on the chinese language data set.

# hmmlearn.py
The main purpose of this code is to prepare a learning model from the training data paased to it via the command line arguments. It counts the number of occurances of each word and tag and their associations that is needed while calculating the joint probability in the viterbi algorithm. It then writes the model that it learns from the training set in the hmmmodel.txt file, after serializing the object.

# hmmdecode.py
The purpose of this file is to read the model provided by the hmmlearn code and use it to calculate the highly probable tag sequence for the sentence. Since it uses viterbi's algorithm, it follows hidden markov model properties - The markov chain property : the probability of a sttate depends on the previous state and the output observation probability only depends on the state that produces the output.

For the markov chain property, we count the number of times a particular tag occurs as the next tag for a given tag. However it might also be possible that there is no such case of a tag occuring a particular tag in our training corpus. To enable smooth working of our code in such cases, we apply laplace smoothing that gives a default value of 1 to all the transitions between two different states(tags).

To keep a track of what is the probability that a sentence will start and end with a particular tag, we also have to introduce 2 custom tags - $@#$START$@#$ and $@#$STOP$@#$, which will help us to find the joint probabilities of the tags that could come up at the beginning or ending of the sentence. Using the Viterbi algorithm, the max probability of each state from previous possible states are stored. The final state/label sequence is then traced back from the stop tag.

# Sample data set
Data sets for two different languages english and chinese are provided. First train the model using the train_tagged file and then use the decoder on the dev_raw file. For checking the accuracy of the code use the tester.py to calculate the accuracy with repect to the dev_tagged file for each language. tester.py expects two command line arguments the output file name and the reference file name. 