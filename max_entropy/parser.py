
from tokenizer import Aggro_Tokenizer, stem_sentence
import ply.yacc as yacc
import sys



tokenizer = Aggro_Tokenizer()
tokens    = Aggro_Tokenizer.tokens


# --- NLP Challenges ---

# - Identify what is really being anded, ored, and negated
# - Identify chances two identifiers are refering to the same thing
# - Support the "it" identifier


# ------------------------
#  - - - Structures - - -
# ------------------------

class Node:


    def __init__ ( self, label, children = [] ):

        self.label = label

        self.children = children

        self.leaf = len( children ) == 0


    def to_str ( self, indentation = 0 ):

        ind = '|  ' * indentation

        string = ind + ( "Leaf: " if self.leaf else "Node: ") + str( self.label )

        for c in self.children:

            string += "\n" + c.to_str( indentation + 1 )

        return string


    def __str__ ( self ):

        return self.to_str()


# -----------------------
#  - - - Variables - - -
# -----------------------




# ------------------------
#  - - - Precedence - - -
# ------------------------

precedence = (
    ('left','EQUALS', 'CMP_LT', 'CMP_GT'),
    ('left','AND','OR'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','POWER'),
    ('nonassoc', 'NOT')
)


# -----------------------------
#  - - - Parser Patterns - - -
# -----------------------------


def p_back_utilization( p ):
    '''utilization : IF proposition THEN proposition'''

    p[0] = Node( p[1] + " " + p[3], [ p[2], p[4] ] )


def p_high_poposition( p ):
    '''proposition : proposition AND proposition
                   | proposition OR  proposition
                   | NOT proposition
    '''

    if len( p ) == 3: #unary

        p[0] = Node( p[1], [ p[2] ] )

    else:

        p[0] = Node( p[2], [ p[1], p[3] ] )


def p_proposition( p ):
    '''proposition : numeric_expression EQUALS EQUALS numeric_expression
                   | numeric_expression EQUALS numeric_expression
                   | numeric_expression inequality numeric_expression
                   | numeric_expression EVENLY
                   | BOOLEAN_CONSTANT
    '''

    if len( p ) == 5: # a equals equals b

        p[0] = Node( p[3], [ p[1], p[4] ] )

    elif len( p ) == 4: # a equals/inequals b

        p[0] = Node( p[2], [ p[1], p[3] ] )

    elif len( p ) == 3: # a evenly

        p[0] = Node( "is", [ Node( "mod", p[1].children ), Node( 0 ) ] )

    else: # boolean const

        p[0] = Node( p[1] )




def p_proper_inequality( p ):
    '''inequality : inequality OR EQUALS
                  | inequality OR EQUALS TO'''

    p[0] = p[1] + " or equal"

def p_inequality_cut_is( p ):

    '''inequality : EQUALS inequality
    '''

    p[0] = p[2]

def p_inequality( p ):
    '''inequality : CMP_LT
                  | CMP_GT
                  | THAN
                  | CMP_LT THAN
                  | CMP_GT THAN'''

    p[0] = p[1]

def p_numeric_expression( p ):
    '''numeric_expression : numeric_expression PLUS   numeric_expression 
                          | numeric_expression MINUS  numeric_expression
                          | numeric_expression TIMES  numeric_expression
                          | numeric_expression DIVIDE numeric_expression
                          | numeric_expression POWER  numeric_expression
                          | numeric_expression MOD    numeric_expression
                          | identifier
                          | numeric_const
    '''
    
    if len( p ) > 2:
        p[0] = Node( p[2], [ p[1], p[3] ] )
    else:
        p[0] = p[1]

def p_numeric_const( p ):
    '''numeric_const : NUMERIC_CONSTANT'''
    p[0] = Node( p[1] )


def p_identifier( p ):
    '''identifier : identifier_content
    '''

    p[0] = Node( '_identifier_', map( Node, p[1] ) )


def p_identifier_content( p ):
    '''identifier_content : UNWORD
                          | UNWORD identifier_content
    '''

    p[0] = [p[1]] + ( p[2] if len(p) > 2 else [] )





# -------------------
#  - - - Main - - -
# -------------------

yacc.yacc()

def main( ):

    ss = stem_sentence("if 2 divides the number n evenly then n is even")

    print ss + "\n"

    print yacc.parse( ss )
    print ""

if __name__ == '__main__':

    main()
