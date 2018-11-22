
import nltk
from nltk.stem.porter import *

import re, pprint



STEMMER_ENABLED = True

class False_Stemmer:
    stem = lambda self, x : x

stemmer = PorterStemmer() if STEMMER_ENABLED else False_Stemmer()



class Preprocessor:

	default_settings = {
		'normalize_case' : True
	}

	def __init__ ( self, settings = {} ):

		self.settings = Preprocessor.default_settings
		self.settings.update( settings )

		self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

		self.tagger = nltk.DefaultTagger('N')

	def stem_word ( self, word ):

	    stop_words = { 'than', 'by' }

	    if word in stop_words:

	    	return None

	    preserve_words = { 'divides' }

	    if word not in preserve_words:

	    	word = stemmer.stem(word)

	    return str(word)

	def prepare ( self, raw ):

		raw = raw.lower()

		sentences = self.sentence_tokenizer.tokenize(raw)

		tokens = [item for sublist in map( nltk.word_tokenize, sentences  ) for item in sublist]

		pos = nltk.pos_tag( tokens )

		stems = map( self.stem_word, tokens )

		pos_positions    = {}
		stemmed_sentence = ''

		current_position = 0
		for i in range( len( tokens ) ):

			if stems[i] is not None:

				pos_positions[current_position] = pos[i]
				current_position += len( stems[i] ) + 1
				
				stemmed_sentence += stems[i] + ' '

		return stemmed_sentence, pos_positions











