

class Code_Object:

	def __init__ ( self, root ):

		self.root = root

		self.name    = ""
		self.code    = ""
		self.arglist = ""
		self.comment = ""

		self.prolog_override = ""

		self.major_rules = []

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


	def gen_code( self, root ):

		code = self.gen_code_helper( root )

		rules = ', '.join( map( lambda rule: '{name}( {args} )'.format(name=rule.name,args=', '.join(rule.arglist)) , code.major_rules ) )

		if code.major_rules:

			rules += ', '

		for q in code.queries:

			q.code = rules + q.code

		code.queries = map( lambda q : q.prolog(), code.queries)

		return code


	def gen_code_helper( self, root ):

		code_obj = Code_Object( root )


		# Recurse

		child_codes = []

		for child in root.children:

			child_obj = self.gen_code_helper( child )

			child_codes.append( child_obj )

			code_obj.major_rules += child_obj.major_rules

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

			code_obj.name = root.alias

			return code_obj

		# Is

		elif root.label == "__is__":

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
				comment   = root.id
			) )



		# Givens, and rules

		elif root.label == "__given__":

			code_obj.major_rules.append( child_codes[0] )

			return code_obj

		elif root.label == "__rule__":

			code_obj.major_rules.append( child_codes[0] )

			return code_obj

		# Queries

		elif root.label == "__query__":

			code_obj.name    = "query_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code    = "{child}( {args} )".format(
				child = child_codes[0].name,
				args  = ', '.join( child_codes[0].arglist ),
			)
			code_obj.comment = root.id

			code_obj.queries.append( code_obj )

			return code_obj



		# Program

		elif root.label == "__program__":

			return code_obj


		# Lines of code

		code_obj.rules.append( code_obj.prolog() )

		return code_obj












