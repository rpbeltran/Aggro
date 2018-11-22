

class Code_Object:

	counter = 0

	def __init__ ( self, label, skip = False ):

		self.prolog = []


		self.identity = "code_object_{counter:x}".format( counter=Code_Object.counter )

		Code_Object.counter += 1


		self.label = label


class Code_Generator:

	def __init__ ( self, ast ):

		self.ast = ast

		self.rules = []

		self.queries = []

	def gen_code( root = self.ast ):

		code_obj = Code_Object( root.label )

		code_child = map( self.gen_code, root.children )


		# Leaves

		if root.leaf:

			assert len( code_child ) == 0


		# Constants

		elif ( root.label == "__numeric const__" ) or ( root.label == "__boolean const__" ):

			assert len( code_child ) == 1

			code_obj.code = "{id}({val}).  /*{label}*/".format(
				label = root.label,
				id  = code_obj.identity,
				val = code_child[0].label
			)


		# Arithmetic

		elif root.label == "__plus__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 + Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif root.label == "__minus__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 - Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)
		
		elif root.label == "__times__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 * Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif root.label == "__divide__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 / Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif root.label == "__power__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 ^ Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif root.label == "__modulo__":

			assert len( code_child ) == 2

			code_obj.code = "{id}(Arg1 mod Arg2) :- {aid}(Arg1), {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		
		# boolean logic

		elif root.label == "__not__":

			assert len( code_child ) == 1

			code_obj.code = "{id}() :- not({aid}()).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity
			)

		elif root.label == "__and__":

			assert len( code_child ) == 2

			code_obj.code = "{id}() :- {aid}(), {bid}().  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif root.label == "__or__":

			assert len( code_child ) == 2

			code_obj.code = "{id}() :- {aid}() ; {bid}().  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		
		# is

		elif root.label == "__is__":

			assert len( code_child ) == 2

			code_obj.code = "{id}() :- {aid}(Arg1), {bid}(Arg2), Arg1 is Arg2.  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)


		# If then structures

		elif root.label == "__if then__":

			if_block, then_block, else_block = None, None, None

			for child_obj in code_child:

				if child_obj.label == "__if__":

					if_block = child_obj

				elif child_obj.label == "__then__":

					then_block = child_obj

			assert if_block   != None
			assert then_block != None

			# If X then Y is equivalent to Not( X and Not( Y ) ) == Not( X ) or Y

			code_obj.code = "{id}() :- not({aid}(Arg1)) ; {bid}(Arg2).  /*{label}*/".format(
				label = root.label,
				id = code_obj.identity,
				aid = code_child[0].identity,
				bid = code_child[1].identity
			)

		elif (root.label == "__if__") or (root.label == "__then__"):

			code_obj.code = "{id}() :- {aid}().  /*{label}*/".format(
				label = root.label,
				id  = code_obj.identity,
				aid = code_child[0].identity
			)


		# givens, and rules
		elif (root.label == "__given__") or (root.label == "__rule__"):

			code_obj.code = "{id}() :- {aid}().  /*{label}*/".format(
				label = root.label,
				id  = code_obj.identity,
				aid = code_child[0].identity
			)

		



		return code_obj



