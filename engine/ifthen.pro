
/* if x is y then z is 2 */

then_action( C ) :- z( 2 ).

if_condition( C ) :- ( x( C ), y( C ) ).

then_action( C ) :- if_condition( C ).










/*

	R1: If x is M, then x is fourly.

	R2: If x is fourly then x is good.

	G1: N is 4.

	G2: M is 4.

	Q: Is N good?

*/


/* G1 */

n( Candidate ) :- Candidate is 4.

/* G2 */

m( Candidate ) :- Candidate is 4.

/* R1 */

is_obj( Candidate ) :- Candidate is 4.

if_cond_1( X ) :- is_obj( X ).

fourly( X ) :- then_action_1( X ).

then_action_1( X ) :- if_cond_1( X ).

/* R2 */

is_cond_2( X ) :- fourly( Candidate ).

if_cond_2( Candidate ) :- fourly( Candidate ).

good( Candidate ) :- then_action_2( Candidate ).

then_action_2( Candidate ) :- if_cond_2( Candidate ).

/* Q */

query_1() :- n( Candidate ), good( Candidate ).





