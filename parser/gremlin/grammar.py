

from algorithms import extended_levenshtein_distance

import regex



class Primitive:

	def __init__ ( self, label, patterns, fuzzy = False, ignore = False ):

		self.label    = label
		self.patterns = patterns

		self.fuzzy  = fuzzy
		self.ignore = ignore

	def matches ( self, token ):

		for pattern in self.patterns:
			if regex.fullmatch( pattern, token ):
				return True

		return False

UNWORD = Primitive( 'UNWORD', r'.*' )


class Chunk:

	def __init__( self, label, patterns, associativity = 'left', ignore = False ):

		self.label    = label
		self.patterns = patterns

		self.associativity = associativity
		self.ignore        = ignore







linear_scoring    = lambda distances : sum( distances )
quadratic_scoring = lambda distances : sum( map( lambda n : n ** 2 ) )


class Grammar:

	def __init__ ( self, primitives, chunks, cost_score = quadratic_scoring ):

		self.primitives = primitives
		self.chunks     = chunks
		self.cost_score = cost_score


	def tag_token( self, token ):

		tag = None

		for primitive in self.primitives:

			if primitive.matches( token ):

				tag = primitive

				break

		return tag if tag is not None else UNWORD

	def tag_tokens( self, tokens ):

		return map( self.tag_token, tokens )


	def score_match ( self, tags, chunk ):

		# Tag primitives

		tags = map( self.tag_token, tokens )

		# Find levenshtein optimal chunking

		print 




_RECURSE = '_RECURSE'


if __name__ == '__main__':

	STARTSET   = Primitive( 'STARTSET', [ r'\{'  ] )
	ENDSET     = Primitive( 'ENDSET',   [ r'\}'  ] )
	COMMA      = Primitive( 'COMMA',    [ r','   ] )
	INTEGER    = Primitive( 'INTEGER',  [ r'\d+' ] )

	set_contents   = Chunk( 'set_contents', [ [ INTEGER ], [ INTEGER, COMMA, _RECURSE ] ] )

	enumerated_set = Chunk( 'enumerated_set', [ [ STARTSET, ENDSET ], [ STARTSET, set_contents, ENDSET ] ] )

	grammar = Grammar( [ STARTSET, ENDSET, COMMA, INTEGER ], [ set_contents, enumerated_set ] )

	tags = grammar.tag_tokens( '{ 1 , 2 , 3 }'.split() )

	print grammar.score_match( tags, enumerated_set )






