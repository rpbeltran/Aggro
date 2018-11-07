% temp.pro
% 11/5/18

hungry(doug).
dog(doug).

bark(X) :- 
	hungry(X)
	,
	dog(X)
.

complicatedbark(X,Y) :-
	hungry(X) , dog(X)
	;
	hungry(Y) , dog(Y)
.





moose(X)  :- false.
duck(X)   :- false.
pigeon(X) :- false.

smelly(X) :- (moose(X) , (moose(Y) , \+ smelly(Y))) ; (\+ moose(X) , smellyhelper(X)).

smellyhelper(X) :- false.

%exist(X) :- true.

moose(flop).
notsmelly(flop).

notsmelly(X) :- \+ smelly(X).