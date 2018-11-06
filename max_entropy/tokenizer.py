
from nltk.stem.porter import *

import sys
import ply.lex as lex



import regex


STEMMER_ENABLED = True

class False_Stemmer:
    stem = lambda self, x : x

stemmer = PorterStemmer() if STEMMER_ENABLED else False_Stemmer()


def gen_token( forms, use_stemmer = False ):

    if use_stemmer:
        forms += map( stemmer.stem, forms )

    return forms


def stop_filter( words ):

    stop_words = { 'a', 'than', 'by' }

    return filter( lambda w : w not in stop_words, words)

def stem_sentence ( sentence ):

    return ' '.join( map( stemmer.stem, stop_filter( sentence.split() ) ) )


class Aggro_Tokenizer:

    configuration = {
        'stemmer': 'porter'
    }


    # --------------------
    #  - - - Tokens - - -
    # --------------------

    reserved = {

        'IF'        : gen_token( ['if'],        True ),
        'THEN'      : gen_token( ['then'],      True ), 
        'ELSE'      : gen_token( ['else'],      True ), 
        'OTHERWISE' : gen_token( ['otherwise'], True ),

        'NOT'    : gen_token(['not'], True ), 
        'AND'    : gen_token(['and'], True ), 
        'OR'     : gen_token(['or'],  True ),

        'PLUS'   : gen_token( [ 'plus', 'add'                 ], True ),
        'MINUS'  : gen_token( [ 'minus', 'subtract'           ], True ),
        'TIMES'  : gen_token( [ 'times', 'multiply'           ], True ),
        'DIVIDE' : gen_token( [ 'divide','over'               ], True ),
        'POWER'  : gen_token( [ 'power', 'power'              ], True ),
        'MOD'    : gen_token( [ 'mod', 'modulus', 'remainder' ], True ),

        'EQUALS' : gen_token(['is','equals'], True ),
        
        'CMP_LT' : gen_token(['less'],    True ),
        'CMP_GT' : gen_token(['greater'], True ),

        'THAN'   : gen_token( [ 'than' ],   True ),
        'BY'     : gen_token( [ 'by' ],     True ),
        'TO'     : gen_token( [ 'to' ],     True ),
        'EVENLY' : gen_token( [ 'evenly' ], True ),

        'BOOLEAN_CONSTANT' : gen_token( ['true', 'false'] )
    }

    tokens = [
        
        'NUMERIC_CONSTANT',
        'UNWORD'

    ] + reserved.keys()

    # ----------------------------
    #  - - - Basic Patterns - - -
    # ----------------------------

    t_ignore = ' \t,.!'


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

        for k in Aggro_Tokenizer.reserved.keys():

            if t.value in Aggro_Tokenizer.reserved[k]:

                t.type = k
                break

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



