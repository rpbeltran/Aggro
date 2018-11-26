
from Tokenizer import Aggro_Tokenizer
import ply.yacc as yacc
import sys


tokenizer = Aggro_Tokenizer()
tokens    = Aggro_Tokenizer.tokens


# ------------------------
#  - - - Structures - - -
# ------------------------

class Node:

    counter = 0

    def __init__ ( self, label, children = [], tags = [] ):

        self.label = label

        self.children = children

        self.leaf = len( children ) == 0

        self.tags = tags

        self.alias = ""

        self.bound = False

        self.phrases = []
        self.givens  = []
        self.rules   = []

        self.id = Node.counter
        Node.counter += 1

        self.label_free()


    def label_free ( self, in_given = False, in_rule = False ):

        if self.label == "__given__":

            in_given = True

        elif self.label == "__rule__":

            in_rule = True

        elif self.label == "__is__":

            if in_given or in_rule:

                if self.children[0].label == "__numeric const__" or self.children[0].bound:

                    if self.children[1].label == "__phrase__":

                        self.children[1].bound = True

                if self.children[1].label == "__numeric const__" or self.children[1].bound:

                    if self.children[0].label == "__phrase__":

                        self.children[0].bound = True

        for child in self.children:

            child.label_free( in_given=in_given, in_rule=in_rule )


    def bind_associated_phrases( self ):

        for p in self.phrases:

            for q in self.phrases:

                if ( p.alias == q.alias ) and q.bound:

                    p.bound = True


    def label_unique_phrases( self ):

        self.unique_phrases = list(set( map( lambda p : p.alias, self.phrases ) ))

        for child in self.children:

            child.label_unique_phrases()


    def place_flags( self ):

        for child in self.children:

            child.place_flags()

        if self.label == "__phrase__":

            self.phrases = [ self ]

        elif not self.leaf:

            self.phrases = [ phrase for child in self.children for phrase in child.phrases ]
        
        if self.label == "__given__":

            self.givens = [ self ]

        elif not self.leaf:

            self.givens = [ phrase for child in self.children for phrase in child.givens ]

        if self.label == "__rule__":

            self.rules = [ self ]

        elif not self.leaf:

            self.rules = [ phrase for child in self.children for phrase in child.rules ]


    def to_str ( self, indentation = 0 ):

        string = '|  ' * indentation

        if self.label == "__phrase__":
            
            string += "Phrase: {{ alias:{alias}, bound:{bound} }} [{id}]".format( id = self.id, alias=self.alias, bound=self.bound )

        elif self.leaf:

            string += "Leaf: {label} [{id}]".format( id = self.id, label = self.label )

        else:

            string += "Node: {label} [{id}]".format( id = self.id, label = self.label )

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

        p[0] = Node( "__query__", [ 
            Node( "__is__", [ p[2], p[3] ] )
        ] )

def p_query2( p ):
    '''sentence : EQUALS identifier SENTENCE_END
                | DOES   identifier SENTENCE_END
    '''

    p[0] = Node( "__query__", [ 
        Node( "__is__", [ 
            Node( "@split", [ p[2] ] ) 
        ] ) 
    ] )


def p_forward_utilization( p ):
    '''sentence : proposition IF proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ 
        Node( "__if then__", [ 
            Node("__if__",   [ p[3] ] ), 
            Node("__then__", [ p[1] ] ) 
        ] ) 
    ] )

def p_forward_utilization2( p ):
    '''sentence : proposition IF AND ONLY IF proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ 
        Node( "__iff then__", [ 
            Node("__if__",   [ p[6] ] ), 
            Node("__then__", [ p[1] ] ) 
        ] ) 
    ] )

def p_forward_utilization3( p ):
    '''sentence : proposition ONLY IF proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ 
        Node( "__iff then__", [ 
            Node("__if__",   [ p[4] ] ), 
            Node("__then__", [ p[1] ] ) 
        ] ) 
    ] )

def p_back_utilization( p ):
    '''sentence : proposition IMPLIES proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ 
        Node( "__if then__", [ 
            Node("__if__",   [ p[1] ] ), 
            Node("__then__", [ p[3] ] ) 
        ] ) 
    ] )

def p_back_utilization2( p ):
    '''sentence : IF proposition THEN proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [ 
        Node( "__if then__", [
            Node("__if__",   [ p[2] ] ), 
            Node("__then__", [ p[4] ] ) 
        ] ) 
    ] )

def p_back_utilization3( p ):
    '''sentence : IF AND ONLY IF proposition THEN proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [
        Node( "__iff then__", [
            Node("__if__",   [ p[5] ] ), 
            Node("__then__", [ p[7] ] ) 
        ] ) 
    ] )

def p_back_utilization4( p ):
    '''sentence : ONLY IF proposition THEN proposition SENTENCE_END'''

    p[0] = Node( "__rule__", [
        Node( "__iff then__", [
            Node("__if__",   [ p[3] ] ), 
            Node("__then__", [ p[5] ] )
        ] ) 
    ] )



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

    p[0] = Node( "__is__", [ 
        Node( "__modulo__", [ p[3], p[1] ] ),
        Node( "__numeric const__", [ Node( 0 ) ] )
    ] )

def p_not_evenly( p ):
    ''' proposition : numeric_expression NOT DIVIDE numeric_expression
                    | numeric_expression NOT DIVIDE numeric_expression EVENLY
    '''

    p[0] = Node( "__not__", [ 
        Node( "__is__", [ 
            Node( "__modulo__", [ p[4], p[1] ] ), 
            Node( "__numeric const__", [ Node( 0 ) ] )
        ] ) 
    ] )

def p_not_evenly2( p ):
    ''' proposition : numeric_expression DOES NOT DIVIDE numeric_expression
                    | numeric_expression DOES NOT DIVIDE numeric_expression EVENLY
    '''

    p[0] = Node( "__not__", [ 
        Node( "__is__", [ 
            Node( "__modulo__", [ p[5], p[1] ] ), 
            Node( "__numeric const__", [ Node( 0 ) ] )
        ] ) 
    ] )

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

    from Preprocessing import Preprocessor

    program = "A year y is a leap year if 4 divides y evenly. Is 2018 a leap year?"

    p = Preprocessor()

    ss, ps = p.prepare( program )

    tokens = tokenizer.tokenize_sentence( ss )

    tree = yacc.parse( ss )

    print ""
    print program
    print ""
    print ss
    print ""
    print tree
    print ""

if __name__ == '__main__':

    main()
