from flask import Flask, render_template, request, redirect, url_for, flash

from functions import Routh_Stability, SolveInequalities, eval_Epsilon

from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, poly, latex, simplify, expand, factor, N, collect
from copy import deepcopy

app = Flask(__name__)

# settings
app.secret_key = 'mysecretkey' 

@app.route("/")
def index():
	return render_template('index.html')



@app.route("/add_poly", methods=['POST'])
def add_poly():
	
	if request.method == 'POST':

		try:

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

			
			
			calc_lim  = bool(len(request.form.getlist("Calculate limits")))#fields.Boolean(request.form["Calculate limits"])
			calc_gain = bool(len(request.form.getlist("Find gain limits")))#fields.Boolean(request.form["Find gain limits"])
			
			#calc_gain = False
			

			# Operations

			Polynomial = poly(parse_expr(polynomia), var)

			P = Polynomial.all_coeffs()


			degree = len(P) 

			Polynomial_Latex = latex( collect(parse_expr(polynomia), var), order = 'lex' )


			P.reverse()


			
			R_array, Notes = Routh_Stability(P, limit_var = epsilon, print_array = False)

			
			
			

			gain_limits_num = "None"
			gain_limits = "None"

			if calc_gain:

				R_array_gain = R_array

				try:

					gain_limits_result = SolveInequalities(SolveInequalities(R_array_gain, gain))

					gain_limits = str(gain) + "\in" + latex(gain_limits_result)

					

					try:
						

						gain_limits_num = str(gain) + "\in" + latex(N(gain_limits_result))
					except:
						
						gain_limits_num = gain_limits


				except :

					try:
						gain_limits_result =  SolveInequalities(R_array_gain, gain, solve_type = 'solve_sets')

						gain_limits = str(gain) + "\in" + latex(gain_limits_result)

						try:

							gain_limits_num = str(gain) + "\in" + latex(N(gain_limits_result))
						except:
							gain_limits_num = gain_limits


					except Exception as e:
						print(e)
						gain_limits = "No Solution found"
						gain_limits_num =  "None"


			if calc_lim:
				R_array = eval_Epsilon(R_array, epsilon)



			# Array elements are converted to strings

			n = len(R_array)
			routh_array_LaTeX = []
			for i in range(n):
				row = R_array[i]
				routh_array_LaTeX.append( [str(var) + "^{" + str(n - 1 - i) + '}:'] + [latex(elem) for elem in row ])


			


			
			return render_template('index.html', Array = routh_array_LaTeX, gain_limits = gain_limits, Polynomial = Polynomial_Latex, Notes = Notes, gain_limits_num = gain_limits_num) #redirect(url_for('index'))

		
		except Exception as e:

			return render_template('index.html',  Notes = ["Unable to parse expression", "Error : " + str(e)])
		

	else:

		pass

@app.route("/calculate")
def calculate():
	return "x^2+x+1"




if __name__ == "__main__":

	app.run(port = 3000, debug = True )