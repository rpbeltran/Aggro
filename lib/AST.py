
from Tokenizer import Aggro_Tokenizer
import ply.yacc as yacc
import sys



tokenizer = Aggro_Tokenizer()
tokens    = Aggro_Tokenizer.tokens


# --- NLP Challenges ---

# - Identify what is really being anded, ored, and negated
# - Identify chances two identifiers are refering to the same thing
# - Support the "it" identifier
# - Inserting implicit "be"s as in "water makes the ground wet" => "water makes the ground be wet"


# ------------------------
#  - - - Structures - - -
# ------------------------

class Node:

    def __init__ ( self, label, children = [], tags = [] ):

        self.label = label

        self.children = children

        self.leaf = len( children ) == 0

        self.tags = tags


    def to_str ( self, indentation = 0 ):

        ind = '|  ' * indentation

        string = ind + ( "Leaf: " if self.leaf else "Node: ") + str( self.label )

        for c in self.children:

            string += "\n" + c.to_str( indentation + 1 )

        return string


    def __str__ ( self ):

        return self.to_str()

    def insert_POS( self, tags ):

        pass


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


def p_program( p ):
    '''program : sentence
               | sentence program
    '''

    if len( p ) == 2:

        p[0] = Node( "__program__", [p[1]] )

    else:

        p[0] = p[2]
        p[0].children.append( p[1] )



def p_given( p ):
    '''sentence : proposition SENTENCE_END'''

    p[0] = Node( "__given__", [p[1]] )


def p_query( p ):
    '''sentence : EQUALS proposition SENTENCE_END 
                | DOES   proposition SENTENCE_END
                | EQUALS numeric_expression numeric_expression SENTENCE_END
    '''
  
    if len( p ) == 4:

      p[0] = Node( "__query__", [p[2]] )

    else:

      p[0] = Node( "__query__", [ Node( "__is__", [ p[2], p[3] ] ) ] )

def p_query2( p ):
    '''sentence : EQUALS identifier SENTENCE_END
                | DOES   identifier SENTENCE_END
    '''

    p[0] = Node( "__query__", [ Node( "__is__", [ Node( "@split", [ p[2] ] ) ] ) ] )


def p_forward_utilization( p ):
    '''sentence : proposition IF proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ Node( "__if then__", [ Node("__if__", [ p[3] ] ), Node("__then__", [ p[1] ] ) ] ) ] )

def p_back_utilization( p ):
    '''sentence : proposition IMPLIES proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ Node( "__if then__", [ Node("__if__", [ p[1] ] ), Node("__then__", [ p[3] ] ) ] ) ] )

def p_back_utilization2( p ):
    '''sentence : IF proposition THEN proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ Node( "__if then__", [ Node("__if__", [ p[2] ] ), Node("__then__", [ p[4] ] ) ] ) ] )



def p_high_poposition( p ):
    '''proposition : proposition AND proposition
                   | NOT proposition
    '''

    if len( p ) == 3: #unary

        p[0] = Node( "__not__", [ p[2] ] )

    else:

        p[0] = Node( "__and__", [ p[1], p[3] ] )

def p_high_poposition2( p ):
    '''proposition : proposition OR proposition
    '''

    p[0] = Node( "__or__", [ p[1], p[3] ] )



def p_evenly( p ):
    '''proposition : numeric_expression DIVIDES numeric_expression 
                   | numeric_expression DIVIDES numeric_expression EVENLY
    '''

    p[0] = Node( "__is__", [ Node( "__modulo__", [ p[1], p[3] ] ), Node( 0 ) ] )

def p_not_evenly( p ):
    ''' proposition : numeric_expression NOT DIVIDE numeric_expression
                    | numeric_expression NOT DIVIDE numeric_expression EVENLY
    '''

    p[0] = Node( "__not__", [ Node( "__is__", [ Node( "__modulo__", [ p[1], p[4] ] ), Node( 0 ) ] ) ] )

def p_not_evenly2( p ):
    ''' proposition : numeric_expression DOES NOT DIVIDE numeric_expression
                    | numeric_expression DOES NOT DIVIDE numeric_expression EVENLY
    '''

    p[0] = Node( "__not__", [ Node( "__is__", [ Node( "__modulo__", [ p[1], p[5] ] ), Node( 0 ) ] ) ] )


def p_proposition( p ):
    '''proposition : numeric_expression EQUALS EQUALS numeric_expression
                   | numeric_expression EQUALS numeric_expression
                   | TRUE
    '''

    if len( p ) == 5: # a equals equals b

        p[0] = Node( "__is__", [ p[1], p[4] ] )

    elif len( p ) == 4: # a equals b

        p[0] = Node( "__is__", [ p[1], p[3] ] )

    else: # boolean const

        p[0] = Node( "__boolean const__", [ Node( "true" ) ] )


def p_proposition2( p ):
    '''proposition : numeric_expression inequality numeric_expression
                   | FALSE
    '''

    if len( p ) == 4:
        p[0] = Node( "__" + p[2] + "__", [ p[1], p[3] ] )
    else:
        p[0] = Node( "__boolean const__", [ Node( "false" ) ] )


def p_improper_inequality( p ):
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

def p_numeric_expression_addition( p ):
    '''numeric_expression : numeric_expression PLUS numeric_expression '''
    
    p[0] = Node( "__plus__", [ p[1], p[3] ] )

def p_numeric_expression_subtraction( p ):
    '''numeric_expression : numeric_expression MINUS numeric_expression '''
    
    p[0] = Node( "__minus__", [ p[1], p[3] ] )

def p_numeric_expression_multiplication( p ):
    '''numeric_expression : numeric_expression TIMES    numeric_expression
                          | numeric_expression TIMES BY numeric_expression
    '''
    if len( p ) == 4:
        p[0] = Node( "__times__", [ p[1], p[3] ] )
    else:
        p[0] = Node( "__times__", [ p[1], p[4] ] )

def p_numeric_expression_division( p ):
    '''numeric_expression : numeric_expression DIVIDE    numeric_expression
                          | numeric_expression DIVIDE BY numeric_expression
    '''
    if len( p ) == 4:
        p[0] = Node( "__division__", [ p[1], p[3] ] )
    else:
        p[0] = Node( "__division__", [ p[1], p[4] ] )

def p_numeric_expression_exponentiation( p ):
    '''numeric_expression : numeric_expression POWER numeric_expression '''
    
    p[0] = Node( "__power__", [ p[1], p[3] ] )

def p_numeric_expression_modulo( p ):
    '''numeric_expression : numeric_expression MOD numeric_expression '''
    
    p[0] = Node( "__modulo__", [ p[1], p[3] ] )


def p_numeric_expression_term ( p ):
    '''numeric_expression : identifier
                          | numeric_const
    '''
    
    p[0] = p[1]

def p_numeric_const( p ):
    '''numeric_const : NUMERIC_CONSTANT'''
    p[0] = Node( "__numeric const__", [ Node( p[1] ) ] )


def p_identifier( p ):
    '''identifier :   identifier_content
                  | A identifier_content
    '''

    if len( p ) == 2:

        p[0] = Node( '__phrase__', map( Node, p[1] ) )

    else:

        p[0] = Node( '__phrase__', map( Node, p[2] ) )
        p[0].tags.append('instantiation')

def p_identifier2( p ):
    '''identifier : THE identifier_content'''

    p[0] = Node( '__phrase__', map( Node, p[2] ) )
    p[0].tags.append('the')


def p_identifier_content( p ):
    '''identifier_content : UNWORD
                          | identifier_content UNWORD
    '''
    if len( p ) == 2:

        p[0] = [ p[1] ]

    else:

        p[0] = [p[2]] + p[1]


def p_error(p):
    if p:
         print("Syntax error at token \"%s\" of type %s"%( p.value, p.type) )
    else:
         print("Syntax error at EOF")




# -------------------
#  - - - Main - - -
# -------------------

yacc.yacc()


def parse( sentence ):

    return yacc.parse( sentence )

def main( ):

    from preprocessing import Preprocessor

    #program = "A year y is a leap year if 4 divides y evenly and y does not divide 100 or y divides 400. The year is 2018. Is y a leap year?"
    program  = "A year y is a leap year if 4 divides y evenly. The year is 2018. Is y a leap year?"

    p = Preprocessor()

    ss, ps = p.prepare( program )

    tokens = tokenizer.tokenize_sentence( ss )

    tree = yacc.parse( ss )

    tree.insert_POS( ps )

    print ""
    print program
    print ""
    print ss
    print ""
    print tree
    print ""

if __name__ == '__main__':

    main()
