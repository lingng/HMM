# Hidden Markov Model
===
###Overview

An immplementation of a Hidden Markov Model part-of-speech tagger for Catalan. The training data is provided tokenized and tagged; the test data will be provided tokenized, and your tagger will add the tags. 

###Data

The uncompressed archive have the following format:

A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.

A file with untagged development data, with words separated by spaces and each sentence on a new line.

A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.

###Programs

Two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. The learning program will be invoked in the following way:

	python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should contain sufficient information for hmmdecode.py to successfully tag new data.

The tagging program will be invoked in the following way:

	python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

###Notes

* Slash character. The slash character ‘/’ is the separator between words and tags, but it also appears within words in the text, so be very careful when separating words from tags. To make life easy, all tags in the data are exactly two characters long.

* Smoothing and unseen words and transitions. You should implement some method to handle unknown vocabulary and unseen transitions in the test data, otherwise your programs won’t work. The unknown vocabulary problem is familiar from your naive Bayes classifier. The unseen transition problem is more subtle: you may find that the test data contains two adjacent unambiguous words (that is, words that can only have one part-of-speech tag), but the transition between these tags was never seen in the training data, so it has a probability of zero; in this case the Viterbi algorithm will have no way to proceed. The reference solution will use add-one smoothing on the transition probabilities and no smoothing on the emission probabilities; for unknown tokens in the test data it will ignore the emission probabilities and use the transition probabilities alone. You may use more sophisticated methods which you implement yourselves.




