
from algorithms.Similarity_Engine import NB_Sim_Engine




def associate_phrases ( phrases, threshold = 0.4 ):

	# Compute a similrity grid

	sim_engine = NB_Sim_Engine()

	for phrase in phrases:

		sim_engine.train( phrase )

	grid = sim_engine.sim_grid( )

	# Todo: split phrases

	# Create an alias table

	alias_table = range( len( phrases ) )

	for i in range( len( alias_table ) ):

		for j in range( len( alias_table ) ):

			if grid[i][j] > threshold:

				alias_table[i] = alias_table[j] = min( alias_table[i], alias_table[j] )

	# Normalize terms to minimum values

	terms = sorted( list( set( alias_table ) ) )

	replacement_head = 0

	for i in range( len( terms ) ):

		if i not in terms:

			for j in range( len( alias_table) ):

				if alias_table[j] == terms[replacement_head]:

					alias_table[j] = i

		replacement_head += 1

	return alias_table



