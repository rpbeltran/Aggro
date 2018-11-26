
from lib.Preprocessing    import Preprocessor

from lib.Tokenizer        import Aggro_Tokenizer

from lib.AST              import parse

from lib.Phrase_Analysis  import *

from lib.Codegen          import Code_Generator

from pyswip.prolog        import *

import os 


def process ( sentence ):

	# Preprocessing

	p = Preprocessor()

	ss, _ = p.prepare( sentence )


	# Tokenization

	tokenizer = Aggro_Tokenizer()

	tokens = tokenizer.tokenize_sentence( ss )


	# Generate

	ast = parse( ss )


	# Phrase Analysis

	ast.place_flags()

	phrases = ast.phrases

	phrases_iters = map( lambda node : [ child.label for child in node.children ], phrases )

	alias_table = associate_phrases( phrases_iters )

	for i in range(len(phrases)):

		phrases[i].alias = "Phrase_{alias}".format( alias = alias_table[i] )

	ast.bind_associated_phrases()
	ast.label_unique_phrases()


	
	# Generate Code

	codegen = Code_Generator( )

	code = codegen.gen_code( ast )


	# Execute Code

	print ""
	print sentence
	print ""
	print ss
	print ""
	print ast
	print ""

	prolog_file = open('aggro_prolog.pro', 'w')
	for rule in code.rules:
		prolog_file.write(rule)
		prolog_file.write("\n")
		print rule
	print ""
	for query in code.queries:
		prolog_file.write(query)
		print query
	prolog_file.close()

	prolog_file = open('aggro_prolog.pro', 'r')

	Prolog.consult("aggro_prolog.pro")
	
	for query in code.queries:
		queryString, rhs = query.split(":", 1)
		prologReturn = list(Prolog.query(queryString))

		print("\n" + queryString + " is:")
		if len(prologReturn) > 0: #MEANS IT IS TRUE
			for res in prologReturn: #IF MULTI-ARGUMENT
				if res:
					for res in prologReturn:
						for key in res:
							print(res[key])
				else:
					print("true")
					return True
		else: # OTHERWISE FALSE
			print("false")
			return False





#process ( "A year is a leapyear if and only if 4 divides the year evenly. The year is 2021. Is the year a leapyear?" )
process ( "If x is 1 then x is y. x is 1. is x a y?" )
