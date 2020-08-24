from sympy.interactive import printing
printing.init_printing(use_latex = True)
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers.inequalities import solve_rational_inequalities
from sympy import *
from math import ceil

#k = symbols("k")# The gain in the system is almost always a real quantity.
#e = symbols("e")



def Routh_Stability(P, limit_var = symbols("ε"), print_array = True):

	"""
	Inputs:

	P:Polinomial expresed as a list
	example: s**2 + 4*s + 1  -> [1, 4, 1]

	limit_var: Variable used to express the epsilon used when one of the elements of the first row of the array is zero

	Output:


	"""
	Notes = [] # List of 

	n = len(P) # Compute the polynomia degree +1
	A = [[0]]*n # Create the array


	#The first two colums of the array are calculated

	A[0] = [P[i] for i in range(n-1, -1,-2)]
	A[1] = [P[i] for i in range(n-2, -1,-2)]

	A[1] = A[1] + [0] * (len(A[0]) - len(A[1]))


	# Now if the degree of the polynomial is high enough we start building the rest of the Routh Array 
	for i in range(2,n):

		A[i] = A[i] + [0] * (len(A[i-1]) - len(A[i]))

		for j in range(1, len(A[i-1])): 


			A[i][j-1] = factor( A[i-1][0] * A[i-2][j] - A[i-2][0] * A[i-1][j] )/(A[i-1][0])



		if all(a == 0 for a in A[i]): # If there is a row of zeros
			P_aux = A[i-1].copy()

			P_new = []

			for elem in P_aux:
				P_new.append(elem)
				P_new.append(0)

			P_new = P_new[0:n-i+1]


			P_new.reverse()

			A[i] = special_derivative(P_new)

			Notes.append("Performed derivation in: \(  s^"+ str(n-i-1) + "  \)  because of full zero row" )

		if A[i][0] == 0: # if one of the elements in the left column is zero
			Notes.append("Zero in: \( s^"+ str(n-i-1) + " \) row in the left column substituted by \(" + str(limit_var) + "\)")
			A[i][0] = limit_var

		A[i] = A[i] + [0] * (len(A[i-1]) - len(A[i]))


		

	if print_array:
		print_Array(A)
	return A, Notes


def print_Array(A):
	"""
	Function used to print a Routh Array in tidy manner
	"""
	n = len(A)-1
	for i in range(n+1):
		elem = A[i]
		print("-"*2*len(str(elem)))
		print("s^"+ str(n-i) + ":" + str(elem))
	

def special_derivative(P):

	"""
	Internal function of 

	"""
	
	dP =  [ P[i] * i  for i in range(1, len(P)) if P[i]!=0]

	dP.reverse()

	return dP



def SolveInequalities(RA, var, solve_type = 'rational'):
	"""
	HA: Routh Array
	var: Sympy variable 

	"""
	sol = S.Reals

	for i in range(len(RA)):
 
		if solve_type == 'rational':

			num, den = fraction(factor(RA[i][0]))
			num = poly(num, var)
			den = poly(den, var)

			sol_it = solve_rational_inequalities([[ (( num, den), '>')]])

		elif solve_type == 'solve_sets':
			
			sol_it = solveset(RA[i][0]>0, var, domain=S.Reals)
		
		sol = Intersection(sol,sol_it)

	return sol


def eval_Epsilon(RA, var):

	for i in range(len(RA)):

		RA[i][0] = limit(RA[i][0], var, 0)


	return RA