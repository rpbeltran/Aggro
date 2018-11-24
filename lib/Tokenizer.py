
import sys
import ply.lex as lex
import regex

from Preprocessing import Preprocessor

preprocessor = Preprocessor()

def gen_token( forms, use_stemmer = False ):

    if use_stemmer:
        forms += map( preprocessor.stem_word, forms )

    return forms

class Aggro_Tokenizer:

    configuration = {
        'stemmer': 'porter'
    }


    # --------------------
    #  - - - Tokens - - -
    # --------------------

    reserved = [ {

        'IF'        : gen_token( [  'if'  ],     True ),
        'THEN'      : gen_token( [ 'then' ],     True ), 
        'ELSE'      : gen_token( [ 'else' ],     True ), 
        'OTHERWISE' : gen_token( [ 'otherwise'], True ),

        'IMPLIES' : gen_token( ['implies', 'makes', 'means'], True ),

        'NOT'    : gen_token([ 'not', 'does not'], True ), 
        'AND'    : gen_token([ 'and' ], True ), 
        'OR'     : gen_token([ 'or'  ], True ),

        'PLUS'    : gen_token( [ 'plus', 'add'       ], True ),
        'MINUS'   : gen_token( [ 'minus', 'subtract' ], True ),
        'TIMES'   : gen_token( [ 'times', 'multiply' ], True ),
        'DIVIDE'  : gen_token( [ 'divide','over'     ], True ),
        'DIVIDES' : gen_token( [ 'divides'           ], True ),
        'POWER'   : gen_token( [ 'power', 'raised'   ], True ),
        'MOD'     : gen_token( [ 'mod', 'modulus', 'remainder' ], True ),

        'EQUALS' : gen_token(['is','are','equals','be'], True ),
        
        'CMP_LT' : gen_token(['less'],    True ),
        'CMP_GT' : gen_token(['greater'], True ),

        'THAN'   : gen_token( [  'than'  ], True ),
        'BY'     : gen_token( [   'by'   ], True ),
        'TO'     : gen_token( [   'to'   ], True ),
        'EVENLY' : gen_token( [ 'evenly' ], True ),

        'TRUE' : gen_token(  ['true' ], True ),
        'FALSE' : gen_token( ['false'], True )
        
    }, {

        'DOES' : gen_token( [  'does'  ], True ),
        'THE' : gen_token ( [  'the'   ], True ),
        'A'    : gen_token( ['a', 'the'], True )

    } ]

    tokens = [
        
        'NUMERIC_CONSTANT',
        'SENTENCE_END',
        'UNWORD'

    ] + sum( [ r.keys() for r in reserved ], [ ] )

    # ----------------------------
    #  - - - Basic Patterns - - -
    # ----------------------------

    t_SENTENCE_END = r'\.|\?|\!'

    t_ignore = ' \t'

    # -----------------------------
    #  - - - Imbued Patterns - - -
    # -----------------------------


    def t_NUMERIC_CONSTANT( self, t ):
        r'-?\d+'

        if t.value[0] == '-':
            t.value = -int(t.value[1:])
        else:
            t.value = int(t.value)

        return t


    # ----------------------
    #  - - - Specials - - -
    # ----------------------

    def t_UNWORD ( self, t ):
        r'[a-z\']+'

        for reserved_list in Aggro_Tokenizer.reserved:

            for k in reserved_list.keys():

                if t.value in reserved_list[k]:

                    t.type = k

                    return t

        return t


    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    def t_error(self, t):
        print( "Illegal character in line %i : '%s'" % ( t.lexer.lineno, t.value[0] ) ) 
        t.lexer.skip(1)


    # -------------------
    #  - - - Lexer - - -
    # -------------------

    # Constructor

    def __init__ ( self ):

        self.build( )

    # Build the lexer

    def build(self,**kwargs):
        
        self.lex = lex.lex(module=self, **kwargs)

    # Tokenize files

    def input(self, data):
        return self.lex.input(str(data))

    def token(self):
        return self.lex.token()

    def tokenize_file( self, filename ):
        
        with open( filename, "r" ) as file:

            return tokenize_sentence( file )

    def tokenize_sentence( self, sentence ):
    
        self.input( sentence )
        
        tokens = []
        while True:
            tok = self.lex.token()
            if not tok:
                break
            tokens.append( tok )

        return tokens

    def tokenize_word( self, sentence ):

        self.input( word )
        return self.lex.token()


# -------------------
#  - - - Main - - -
# -------------------

if __name__ == '__main__':

    tokenizer = Aggro_Tokenizer()

    stemmed_input = ' '.join( map( stemmer.stem, stop_filter( "year y divide 1 than 1".split() ) ) )

    for t in tokenizer.tokenize_sentence( stemmed_input ):
        print t



