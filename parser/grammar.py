
# Goals: utilizations of high level expressions of logical operations atop independent propositions


# Features not supported:
#    * high_expressions implying high expressions
#    * Context-dependent referencial utilizations




### Tokens

'''
IF
THEN
OTHERWISE

AND
OR

DIVIDES
EVENLY

CMP_EQ
CMP_LT
CMP_GT
CMP_LE
CMP_GE

BOOLEAN_CONSTANT
NUMERIC_CONSTANT

IDENTIFIER
TYPE
'''


### Chunks


'''
utilization : forward_utilization | backward_utilization
'''

'''
forward_utilization : proposition IF high_expression
'''

'''
backward_utilization : IF high_expression THEN proposition
                     | proposition makes proposition
'''

'''
high_expression : proposition
				| high_expression boolean_bin_op high_expression
				| NOT high_expression
'''


'''
high_functor : proposition bin_op
             | proposition bin_op high_functor 
'''

'''
boolean_bin_op : AND | OR
'''

'''
proposition : numeric_expression CMP_EQ numeric_expression
            | numeric_expression CMP_LT numeric_expression
            | numeric_expression CMP_GT numeric_expression
            | numeric_expression CMP_LE numeric_expression
            | numeric_expression CMP_GE numeric_expression

            | numeric_expression DIVIDES numeric_expression
            | numeric_expression DIVIDES numeric_expression EVENLY

            | variable HOLDS variable

            | BOOLEAN_CONSTANT
'''

'''
numeric_expression : numeric_expression numeric_bin_op numeric_expression

                   | NUMERIC_CONSTANT
'''


'''
numeric_bin_op : PLUS | MINUS | TIMES | DIVIDE_BY | POWER_OF | MOD
'''

'''
variable : IDENTIFIER
         | IDENTIFIER IDENTIFIER
         | IDENTIFIER IDENTIFIER IDENTIFIER
'''



# Example:

# "A year y is a leap year if 4 divides y evenly and y does not divide 100 or y divides 400. Is 2012 a leap year?"
# Tokens: 
#     "year"/type "y"/IDENTIFIER  "is"/HOLDS  "leap year"/IDENTIFIER  "if"/IF  "4"/NUMERIC_CONSTANT  "divides"/DIVIDES  "y"/IDENTIFIER  "evenly"/EVENLY ...



