
from math import log

from levenshtein import extended_levenshtein_distance


class NB_Sim_Engine:

	def __init__ ( self, phrases = None ):

		self.argcount = {}
		self.doccount = {}

		self.phrase_count = 0

		self.vocab = set([])

		self.phrases = []

		if phrases != None:

			for p in phrases:

				self.train( p )


	def train ( self, phrase ):

		if phrase in self.phrases:

			self.phrases.append( phrase )

			return

		self.phrases.append( phrase )

		for x in set( phrase ):

			self.vocab.add( x )

			if not x in self.doccount:

				self.doccount[x] = 0

			self.doccount[x] += 1

			for y in set( phrase ):

				if not (x,y) in self.doccount:

					self.doccount[(x,y)] = 0

				self.doccount[(x,y)] += 1

		for a in phrase:

			if not a in self.argcount:

				self.argcount[ a ] = 0

			self.argcount[   a   ] += 1

			for b in phrase:

				if not (a,b) in self.argcount:

					self.argcount[ (a,b) ] = 0
				
				self.argcount[ (a,b) ] += 1

		self.phrase_count += 1


	def p1( self, x ):

		if ( type( x ) == list ):

			p = 1

			for i in set( x ):

				p *= self.p1( i )

			return p

		count = 1.0 + float( self.doccount[x] if x in self.doccount else 0 )

		return count / ( 1 + self.phrase_count )


	def p2( self, x, y ):

		return self.p1( x + y ) / self.p1( y )


	def p( self, *args ):

		return self.p1( args[0] ) if len( args ) == 1 else self.p2( args[0], args[1])


	def similarity( self, X, Y ):

		probability_measure = ( self.p2( X, Y ) ** 2 ) * self.p1( Y ) / self.p1( X )

		overlap = 0
		for x in X:
			if x in Y:
				overlap += 1.0

		overlap_measure = overlap / min( len( X ), len( Y ) )

		return overlap_measure * ( probability_measure ** .5 )


	def sim_grid( self, prettify = False ):

		grid = [ [] for p in self.phrases ]

		for row in range( len( self.phrases ) ):

			for col in range(len(self.phrases)):

				grid[row].append( self.similarity( self.phrases[row], self.phrases[col] ) )

		if not prettify:

			return grid

		for row in range(len(self.phrases)):

			for col in range(len(self.phrases)):

				grid[row][col] = int( 100 * grid[row][col] )

		return grid





if __name__ == '__main__':
	
	A = [ "year", "y"    ]
	B = [ "leap", "year" ]
	C = [ "y" ]

	engine = NB_Sim_Engine( [A,B,C] )

	print engine.sim_grid( True )

