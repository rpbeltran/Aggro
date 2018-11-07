from pyswip import Prolog

#CONSULT 1 FILE BY CALLING IT LIKE SO
#THIS ENABLES THE USE OF ITS FUNCTIONS LATER
Prolog.consult("temp.pro")

#IF YOU CONSULT A SECOND FILE, THAT'LL OVERWRITE YOUR OLD CONSULT
#THIS MEANS YOU SHOULD HAVE ALL CONSULTATIONS IN 1 FILE
#Prolog.consult('temp2.pro')

#YOU CAN MAKE SIMPLE ASSERTIONS HERE ASWELL.
#I'M NOT SURE IF THESE WILL BE USEFUL FOR US.
Prolog.assertz("dog(fido)")
Prolog.assertz('hungry(fido)')



#A SIMPLE RETURN FOR ALL THINGS X THAT SATISFY BARK
#IF YOU QUERY LIKE bark(doug) IT DOES NOT RETURN T/F
	#FOR SOME REASON THIS FUNCTIONALITY ISN'T SUPPORTED
	#WE WILL NEED TO ADD THIS OURSELVES IF WE WANT IT
print("NORMAL BARK CONTESTANTS INCOMING!")
for res in Prolog.query("bark(X)."):
	print(res["X"])

#A MORE COMPLICATED CALL FOR ALL THINGS X,Y THAT SATISFY A COMPLICATEDBARK
print("\nCOMPLICATED BARK CONTESTANTS INCOMING!")
for res in Prolog.query("complicatedbark(X,Y)"):
	print(res["X"],end=" VS ")
	print(res["Y"])

#Prolog.assertz("duck(paddiwack)")
#Prolog.assertz("moose(fk)")

#AGAIN YOU CAN LIMIT THE COMPLICATED CALL, BUT STILL USE IT THE SAME WAY!
print("\nCOMPLICATED BARK WITH DOUG CONTESTANTS INCOMING!")
for res in Prolog.query("complicatedbark(doug,Y) , (moose(X) ; duck(X))"):
	print(res["Y"])
	print(res)