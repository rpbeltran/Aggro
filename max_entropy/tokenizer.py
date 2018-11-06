

import sys
import ply.lex as lex

from nltk.stem.porter import *


STEMMER_ENABLED = False

class False_Stemmer:
    stem = lambda self, x : x

stemmer = PorterStemmer() if STEMMER_ENABLED else False_Stemmer()


def gen_token( forms, use_stemmer = False ):

    if use_stemmer:
        forms = map( stemmer.stem, forms )

    forms = map( lambda form : '(' + form + ')', forms )

    return '|'.join( forms )


def stop_filter( words ):

    stop_words = { 'a' }

    return filter( lambda w : w not in stop_words, words)


class Aggro_Tokenizer:

    configuration = {
        'stemmer': 'porter'
    }


    # --------------------
    #  - - - Tokens - - -
    # --------------------

    tokens = (
        'IF','THEN', 'ELSE', 'OTHERWISE',
        'NOT', 'AND', 'OR',
        'PLUS','MINUS','TIMES','DIVIDE','POWER','MOD','BY',
        'EQUALS', 'CMP_LT', 'CMP_GT', 'THAN', 'TO', 'EVENLY',
        'BOOLEAN_CONSTANT', 'NUMERIC_CONSTANT',
        'UNWORD'
    )

    # ----------------------------
    #  - - - Basic Patterns - - -
    # ----------------------------

    t_IF        = gen_token( ['if'],        True )
    t_THEN      = gen_token( ['then'],      True )
    t_ELSE      = gen_token( ['else'],      True )
    t_OTHERWISE = gen_token( ['otherwise'], True )

    t_PLUS    = gen_token( [ 'plus', 'add'       ], True )
    t_MINUS   = gen_token( [ 'minus', 'subtract' ], True )
    t_TIMES   = gen_token( [ 'times', 'multiply' ], True )
    t_DIVIDE  = gen_token( [ 'divide','over'     ], True )
    t_POWER   = gen_token( [ 'power', 'power'    ], True )
    t_MOD     = gen_token( [ 'mod', 'modulus', 'remainder' ], True )
    t_EVENLY  = gen_token( [ 'evenly' ], True )
    t_THAN    = gen_token( [ 'than' ], True )
    t_TO      = gen_token( [ 'to' ], True )

    t_NOT = gen_token(['not'], True )
    t_AND = gen_token(['and'], True )
    t_OR  = gen_token(['or'],  True )

    t_EQUALS = gen_token(['is','equals'], True )
    t_CMP_LT = gen_token(['less'],    True )
    t_CMP_GT = gen_token(['greater'], True )

    t_BOOLEAN_CONSTANT = r'true|false'

    t_UNWORD = r'[a-z\']+'

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



