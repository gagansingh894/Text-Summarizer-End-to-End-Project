import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm
from heapq import nlargest

class Summarizer(object):

    def __init__(self, document):
        self.document = document
        self.stopwords = list(STOP_WORDS)
        self.nlp = en_core_web_sm.load()
        self.docx = self.nlp(self.document)
        self.word_frequencies = {}        
        self.maximum_frequency = -1
        self.sentence_scores = {}
        
    def summarize(self):
        self._tokenization()
        self._calculate_word_probability()
        self._calculate_sentence_scores()

        self.summarized_sentences = nlargest(7, self.sentence_scores, key=self.sentence_scores.get)
        self.summary = [ w.text for w in self.summarized_sentences ]
        self.summary = ' '.join(self.summary)

        return self.summary    

    def _tokenization(self):    
        for word in self.docx:
            if word.text not in self.stopwords:
                if word.text not in [' ', '  ', '   ']:
                    if word.text not in self.word_frequencies.keys():
                        self.word_frequencies[word.text] = 1
                    else:
                        self.word_frequencies[word.text] += 1

        self.maximum_frequency = max(self.word_frequencies.values())
        
        return self

    def _calculate_word_probability(self):
        for word in self.word_frequencies.keys():
           self. word_frequencies[word] = (self.word_frequencies[word]/self.maximum_frequency)
        return self

    def _calculate_sentence_scores(self):
        self.sentance_list = [ sentence for sentence in self.docx.sents ]
        for sent in self.sentance_list:
            for word in sent:
                if word.text.lower() in self.word_frequencies.keys():
                    if len(sent.text.split(' ')) < 30:
                        if sent not in self.sentence_scores.keys():
                            self.sentence_scores[sent] = self.word_frequencies[word.text.lower()]
                        else:
                            self.sentence_scores[sent] += self.word_frequencies[word.text.lower()]

        return self



# test_document = 'Machine learning (ML) is the study of computer algorithms that improve automatically through experience.[1][2] It is seen as a subset of artificial intelligence. Machine learning algorithms build a mathematical model based on sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to do so.[3] Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning.[5][6] In its application across business problems, machine learning is also referred to as predictive analytics.'
# summarizer = Summarizer(test_document)
# summarizer.summarize()
