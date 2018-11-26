

class Code_Object:

	def __init__ ( self, root ):

		self.root = root

		self.name    = ""
		self.code    = ""
		self.arglist = ""
		self.comment = ""

		self.prolog_override = ""

		self.major_rules = []

		self.free_rules  = []

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

		givens = ', '.join( map( lambda rule: '{name}( {args} )'.format(name=rule.name,args=', '.join(rule.arglist)) , code.major_rules ) )

		if code.major_rules:

			givens += ', '

		for query in code.queries:

			query.code = givens + query.code

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
			code_obj.free_rules += child_obj.free_rules

			code_obj.rules   += child_obj.rules
			code_obj.queries += child_obj.queries

		
		# Leaves

		if root.leaf:

			return code_obj

		# Constants

		elif root.label in ( "__numeric const__", "__boolean const__" ):

			code_obj.name    = "const_{id}".format(id=root.id)
			code_obj.arglist = [ "Candidate".format( id=root.id ) ]
			code_obj.code    = "Candidate is {val}".format(
				id  = root.id,
				val = child_codes[0].root.label
			)
			code_obj.comment = root.id

		# Constants

		elif root.label == "__phrase__":

			code_obj.name = root.alias

			return code_obj

		# Arithmetic

		elif root.label in ( "__plus__", "__minus__", "__times__", "__divide__", "__power__", "__modulo__" ):

			op = { "__plus__" : '+', "__minus__" : '-', "__times__" : '*', "__divide__" : '/', "__power__" : '^', "__modulo__" : 'mod' }[root.label]

			code_obj.name    = "arithmetic_{id}".format(id=root.id)
			code_obj.arglist = [ "Candidate".format(id=root.id) ]

			if child_codes[0].root.label != "__phrase__" and child_codes[1].root.label != "__phrase__":

				code_obj.code = "{aid}(Arg1), {bid}(Arg2), Candidate is (Arg1 {op} Arg2)".format(
					id = root.id,
					op = op,
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)

			elif child_codes[0].root.label == "__phrase__" and child_codes[1].root.label != "__phrase__":

				code_obj.arglist.append( child_codes[0].name )

				code_obj.code = "{bid}(Arg2), Candidate is ({aid} {op} Arg2)".format(
					id = root.id,
					op = op,
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)

			elif child_codes[0].root.label != "__phrase__" and child_codes[1].root.label == "__phrase__":

				code_obj.arglist.append( child_codes[1].name )

				code_obj.code = "{aid}(Arg1), Candidate is (Arg1 {op} {bid})".format(
					id = root.id,
					op = op,
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)

			else:

				code_obj.arglist.append( child_codes[0].name )
				code_obj.arglist.append( child_codes[1].name )

				code_obj.code = "Candidate is ({aid} {op} {bid})".format(
					id = root.id,
					op = op,
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)

			code_obj.comment = root.id

		# Is

		elif root.label == "__is__":

			if child_codes[0].root.label == "__phrase__" and child_codes[1].root.label == "__phrase__":

				code_obj.name    = "is_{id}".format(id=root.id)
				code_obj.arglist = root.unique_phrases
				code_obj.set_prolog( '{name}( A, A ).'.format(
					name   = code_obj.name
				) )

			elif child_codes[0].root.label == "__phrase__" and child_codes[1].root.label != "__phrase__":

				code_obj.name    = "is_{id}".format(id=root.id)
				code_obj.arglist = root.unique_phrases
				code_obj.code    = "{bid}( {aid} )".format(
					aid = ', '.join(child_codes[1].arglist).replace( 'Candidate', child_codes[0].name ),
					bid = child_codes[1].name
				)
				code_obj.comment = root.id
		
			elif child_codes[0].root.label != "__phrase__" and child_codes[1].root.label == "__phrase__":

				code_obj.name    = "is_{id}".format(id=root.id)
				code_obj.arglist = root.unique_phrases
				code_obj.code    = "{aid}( {bid} )".format(
					aid = child_codes[0].name,
					bid = child_codes[1].name
				)
				code_obj.comment = root.id

			else:

				code_obj.name    = "is_{id}".format(id=root.id)
				code_obj.arglist = root.unique_phrases
				code_obj.code    = "{aid}( {a_arg} ), {bid}( {b_arg} )".format(
					aid = child_codes[0].name,
					a_arg = ', '.join(child_codes[0].arglist),
					bid = child_codes[1].name,
					b_arg = ', '.join(child_codes[1].arglist)
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

			code_obj.name = "if_then_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code = '( {if_name}( {if_args} ), {then_name}( {then_args} ) ) | not( {if_name}( {if_args} ) )'.format(
				if_name = if_obj.name,
				if_args = ', '.join( if_obj.arglist ),
				then_name = then_obj.name,
				then_args = ', '.join( then_obj.arglist )
			)
			code_obj.comment = root.id

		elif root.label == "__iff then__":

			if_obj, then_obj = child_codes

			code_obj.name = "iff_then_{id}".format(id=root.id)
			code_obj.arglist = root.unique_phrases
			code_obj.code = '( {if_name}( {if_args} ), {then_name}( {then_args} ) ) | ( not( {if_name}( {if_args} ) ), not( {then_name}( {then_args} ) ) )'.format(
				if_name = if_obj.name,
				if_args = ', '.join( if_obj.arglist ),
				then_name = then_obj.name,
				then_args = ', '.join( then_obj.arglist )
			)
			code_obj.comment = root.id

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
			code_obj.arglist = []
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












