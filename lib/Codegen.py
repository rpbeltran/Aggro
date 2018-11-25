

class Code_Object:

	def __init__ ( self, root ):

		self.root = root

		self.name    = ""
		self.code    = ""
		self.arglist = ""
		self.comment = ""

		self.prolog_override = ""

		self.rules   = []
		self.queries = []
		

	def set_prolog( self, prolog ):

		self.prolog_override = prolog

	def prolog( self ):

		if self.prolog_override:

			return self.prolog_override

		return '{name}( {arglist} ) :- {body}.{comment}'.format(
			name    = self.name,
			arglist = ', '.join(self.arglist),
			body    = self.code,
			comment = ' /*{comment}*/'.format(comment=self.comment) if self.comment else ""
		)



class Code_Generator:

	def __init__ ( self ):

		self.rules = []

		self.queries = []

	def gen_code( self, root = None ):

		if root == None:

			root = self.ast


		code_obj = Code_Object( root )


		# Recurse

		child_codes = []

		for child in root.children:

			child_obj = self.gen_code( child )

			child_codes.append( child_obj )

			code_obj.rules   += child_obj.rules
			code_obj.queries += child_obj.queries

		
		# Leaves

		if root.leaf:

			return code_obj

		# Constants

		elif root.label in ( "__numeric const__", "__boolean const__" ):

			code_obj.name    = "const_{id}".format(id=root.id)
			code_obj.arglist = [ "Candidate" ]
			code_obj.code    = "Candidate is {val}".format(
				val = child_codes[0].root.label
			)
			code_obj.comment = root.id

		# Constants

		elif root.label == "__phrase__":

			code_obj.name = root.alias.lower()

			return code_obj

		# Is

		elif root.label == "__is__":

			if child_codes[0].root.label == "__phrase__" and child_codes[1].root.label == "__phrase__":

				code_obj.name    = child_codes[0].name
				code_obj.arglist = [ 'Candidate' ]
				code_obj.code = "{right}( Candidate )".format(
					right = child_codes[1].name
				)

				code_obj_rev = Code_Object()

				code_obj_rev.name       = child_codes[1].name
				code_obj_rev.arglist    = [ 'Candidate' ]
				code_obj_rev.code = "{right}( Candidate )".format(
					right = child_codes[0].name
				)

				code_obj_rev.rules.append( code_obj.prolog() )
				code_obj_rev.rules.append( code_obj_rev.prolog() )

				return code_obj

			else:

				if child_codes[0].root.label == "__phrase__":

					child_codes[0].arglist = [ 'Candidate' ]
					child_codes[0].code    = "{val}(Candidate)".format(
						val = child_codes[1].name
					)

					code_obj.rules.append( child_codes[0].prolog() )

				elif child_codes[1].root.label == "__phrase__":

					child_codes[1].arglist = [ 'Candidate' ]
					child_codes[1].code    = "{val}(Candidate)".format(
						val = child_codes[1].name
					)

					code_obj.rules.append( child_codes[1].prolog() )

				code_obj.name    = "is_{id}".format(id=root.id)
				code_obj.arglist = root.unique_phrases
				code_obj.code    = "{bid}( {aid} )".format(
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)
				code_obj.comment = root.id

		# If ___ then ___

		elif root.label == "__if__":

			code_obj.name    = "if_cond_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code    = "{cond}( {args} )".format(
				cond = child_codes[0].name,
				args = ', '.join( child_codes[0].arglist )
			)
			code_obj.comment = root.id

		elif root.label == "__then__":

			code_obj.name    = "then_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code    = "{cond}( {args} )".format(
				cond = child_codes[0].name,
				args = ', '.join( child_codes[0].arglist )
			)
			code_obj.comment = root.id

		elif root.label == "__if then__":

			if_obj, then_obj = child_codes

			code_obj.set_prolog( '{then_code} :- {if_code}. /* {comment} */'.format(
				if_code   = if_obj.code,
				then_code = then_obj.code,
				comment = root.id
			) )



		# Givens, and rules

		elif root.label == "__given__":

			return code_obj

		elif root.label == "__rule__":

			return code_obj

		# Queries

		elif root.label == "__query__":

			code_obj.name    = "query_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code    = "{child}( {args} )".format(
				child = child_codes[0].name,
				args  = ', '.join( child_codes[0].arglist )
			)
			code_obj.comment = root.id



		# Program

		elif root.label == "__program__":

			return code_obj


		# Lines of code

		code_obj.rules.append( code_obj.prolog() )

		return code_obj












