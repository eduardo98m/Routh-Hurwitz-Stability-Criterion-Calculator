from flask import Flask, render_template, request, redirect, url_for, flash

from functions import Routh_Stability, SolveInequalities, eval_Epsilon

from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, poly, latex, simplify, expand, factor, N, collect

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey' 

@app.route("/")
def index():
	return render_template('index.html')



@app.route("/add_poly", methods=['POST'])
def add_poly():
	
	if request.method == 'POST':

		# Web

		polynomia = request.form["poly"]
		var = request.form["var"]
		if var:
			var = symbols(var)
		else:
			var =  symbols("s")

		gain = request.form["gain"]
		
		if gain:
			gain = symbols(gain)
		else:
			gain =  symbols("k")

		epsilon = request.form["epsilon"]
		
		if epsilon:
			epsilon = symbols(epsilon)
		else:
			epsilon =  symbols("ε")
		

		


		# Operations

		Polynomial = poly(parse_expr(polynomia), var)

		P = Polynomial.all_coeffs()


		degree = len(P) 

		Polynomial_Latex = latex( collect(parse_expr(polynomia), var), order = 'lex' )

		print(Polynomial)
		#help(Polynomial)

		P.reverse()


		if epsilon:
			R_array = eval_Epsilon(Routh_Stability(P, limit_var = epsilon, print_array = False), epsilon)
		else:
			R_array = Routh_Stability(P, print_array = False)


		try:

			gain_limits = str(gain) + "\in" + latex(SolveInequalities(R_array, gain))

		except:

			try:

				gain_limits = str(gain) + "\in" + latex(SolveInequalities(R_array, gain, solve_type = 'solve_sets'))


			except:
				gain_limits = "No Solution found"



		# Array elements are converted to strings

		n = len(R_array)
		routh_array_LaTeX = []
		for i in range(n):
			row = R_array[i]
			routh_array_LaTeX.append( [str(var) + "^{" + str(n - 1 - i) + '}:'] + [latex(elem) for elem in row ])



		#flash(R_array)






		return render_template('index.html', Array = routh_array_LaTeX, gain_limits = gain_limits, Polynomial = Polynomial_Latex) #redirect(url_for('index'))

	else:

		pass

@app.route("/calculate")
def calculate():
	return "x^2+x+1"




if __name__ == "__main__":

	app.run(port = 3000, debug = True )