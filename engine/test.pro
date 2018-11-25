

then_action( Z ) :- Z is 2.

if_condition( X, Y ) :- X is Y.

if_then( X, Y, Z ) :- then_action( Z ) | not( if_condition( X, Y ) ).