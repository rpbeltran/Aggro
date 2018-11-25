
from lib.Preprocessing    import Preprocessor

from lib.Tokenizer        import Aggro_Tokenizer

from lib.AST              import parse

from lib.Phrase_Analysis  import *

from lib.Codegen          import Code_Generator



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

	phrases_iters = map( lambda node : [ str(child) for child in node.children ], phrases )

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
	for rule in code.rules:
		print rule




process( "x is y." )
#process ( "y is a leapyear if 4 divides y evenly. The year is 2018. Is the year a leapyear?" )
