
def extended_levenshtein_distance ( a, b, insert_cost = 1, replace_cost = 1, delete_cost = 1, allow_insertion = True, allow_replacement = True, allow_deletion = True ):

    infinite = 'INF'

    A, B = len(a), len(b)

    # Define a dynamic programming table

    table = [ [ 0 for i in range( A + 1 ) ] for j in range( B + 1 ) ]

    # Initialize first row and column by assuming pure deletion

    for i in range( A + 1):

        table[0][i] = i * delete_cost if allow_deletion else infinite
    
    for j in range( B + 1):

        table[j][0] = j * insert_cost if allow_insertion else infinite

    # Iterate unfilled cells in table from top left to bottom right

    for i in range( 1, A + 1 ):

        for j in range( 1, B + 1 ):

            if a[i-1] == b[j-1]:

                table[j][i] = table[j-1][i-1]

            else:

                choices = []
                
                if allow_replacement:
                    choices.append( table[j-1][i-1] + replace_cost )

                if allow_deletion:
                    choices.append( table[j-1][i] + delete_cost )

                if allow_insertion:
                    choices.append( table[j][i-1] + insert_cost )

                table[j][i] = min( choices ) if len( choices ) > 0  else infinite

    return table[B][A] if table[B][A] != infinite else -1

