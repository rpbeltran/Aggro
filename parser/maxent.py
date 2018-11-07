

class Feature:

	default_args = { 
		'rule' : (lambda d:False),
		'weight' : 1
	}

	def __init__ ( self, _args = {} ):

		args = Feature.default_args
		args.update( _args )

		self.rule   = args['rule']
		self.weight = args['weight']



class Maximum_Entropy:

	def __init__ ( self, classes ):

		self.classes  = classes
		self.rules    = []
		self.features = { c:[] for c in self.classes }


	def best_classification( self, document ):

		best_c = None

		for c in self.classes:

			score = sum( [ feature.weight for feature in filter( lambda f : f.rule( document ), self.features[c] ) ] )

			if best_c == None or score > best_score:

				best_c = c
				best_score = score

			print c, score

		return best_c

	def add_feature( self, classification, **args ):

		self.features[classification].append( Feature( args ) )



if __name__ == '__main__':

	maxent = Maximum_Entropy( ['C1', 'C2', 'C3' ] )

	maxent.add_feature('C1',
		rule = lambda d : d[0] == '1'
	)

	maxent.add_feature('C2',
		rule = lambda d : d[0] == '2'
	)

	maxent.add_feature('C3',
		rule = lambda d : d[0] == '3'
	)

	maxent.add_feature('C3',
		rule = lambda d : True,
		weight = .1
	)

	print maxent.best_classification( '0123' )