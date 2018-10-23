

/*
	Set functions in Prolog
*/

compress( Raw, Compressed ) :- compress( Raw, Compressed, [] ).

compress( [], Compressed, Compressed ).

compress( [H|[H|T]], Compressed, Acc ) :- compress( [H|T], CTail ), append( Acc, CTail, Compressed ).
compress( [H|T],     Compressed, Acc ) :- compress( T, CTail ), append( Acc, [H|CTail], Compressed ).


/* Set Constructor

	set( List, Set )

*/

set( L, S ) :- sort( L, S ), compress( L, S ).


/* Set Membership 

	member( candidate, set )

*/

member( X, [X|_] ).
member( X, [_|T] ) :- member( X, T ).


/* Subset

	subset( A, B )

*/

subset( [], _ ).
subset( [X], Y )   :- member( X, Y ), !.
subset( [X|T], Y ) :- member( X, Y), subset( T, Y ).


/* Union 

	union( A, B, AuB )

*/

union( A, B, AuB ) :- union( A, B, AuB, [] ).

union( [],    _, AuB, Acc ) :- sorted( Acc, AuB ).
union( [X|T], B, AuB, Acc ) :- member( C, B ), union( T, B, AuB, Acc ).
union( [_|T], B, AuB, Acc ) :- union( T, B, AuB, Acc ).


/* Intersection 

	union( A, B, AnB )

*/

intersection( A, B, AnB ) :- intersection( A, B, AnB, [] ).

intersection( _, [], AnB, AnB ).
intersection( [], _, AnB, AnB ).

intersection( [H|Atail], [H|Btail], AnB, Acc ) :- 
	append( Acc, [H], Acc2 ), 
	intersection( Atail, Btail, AuB, Acc2 ).

intersection( [Ahead|Atail], [Bhead|Btail], AnB, Acc ) :- 
	Ahead < Bhead,
	intersection( Atail, [Bhead|Btail], AnB, Acc ).

intersection( [Ahead|Atail], [Bhead|Btail], AnB, Acc ) :- 
	intersection( [Ahead|Atail], Btail, AnB, Acc ).



/* Compliment

	compliment( A, B, C ) 
	A - B = C

*/

compliment( A, B, C ) :- Compliment( A, B, C, [] ).

compliment( A, [], C, Acc ):- append( Acc, A, C ).
compliment( [], _, C, C )  :- .

compliment( [H|Atail], [H|Btail], AnB, Acc ) :- compliment( Atail, Btail, AuB, Acc ).

compliment( [Ahead|Atail], [Bhead|Btail], AnB, Acc ) :- 
	Ahead < Bhead,
	compliment( Atail, [Bhead|Btail], AnB, Acc ).

compliment( [Ahead|Atail], [Bhead|Btail], AnB, Acc ) :- 
	compliment( [Ahead|Atail], Btail, AnB, Acc ).







