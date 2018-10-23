
from __future__ import division

import nltk

import re, pprint



class Tokenized_Data :

	def __init__ ( self, raw, sentences, tokens, texts, pos ):

		self.raw = raw

		self.sentences = sentences
		self.tokens    = tokens
		self.texts     = texts
		self.pos       = pos




class Tokenizer:

	default_settings = {
		'normalize_case' : False
	}

	def __init__ ( self, settings = {} ):

		self.settings = Tokenizer.default_settings
		self.settings.update( settings )

		self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

		self.tagger = nltk.DefaultTagger('N')

	def tokenize( self, raw ):

		sentences = self.sentence_tokenizer.tokenize(raw)

		tokens = map( lambda sentence : nltk.word_tokenize( sentence.lower() if self.settings['normalize_case'] else sentence ), sentences )

		nltk_texts = map( lambda toks: nltk.Text(toks), tokens )

		pos = map( lambda text : nltk.pos_tag(text), nltk_texts )

		return Tokenized_Data( raw, sentences, tokens, nltk_texts, pos )

