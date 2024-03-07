from sympy import symbols, Expr
from sympy.utilities.lambdify import implemented_function
from sympy import lambdify
import sympy.geometry as geo
import numpy as np
import matplotlib.pyplot as plt


def get_plotter(obj):
	if isinstance(obj, geo.Polygon):
		return plot_polygon
	elif isinstance(obj, geo.Circle):
		return plot_circle
	elif isinstance(obj, Expr):
		return plot_expression
	else:
		return None


def get_default_axes():
	_, axes = plt.subplots(1)
	axes.set_aspect(1)
	return axes

def plot_expression(obj, axes, **kwargs):
	x_vals = np.linspace(-10, 10, 100)
	fn = lambdify(symbols('x'), obj)
	y_vals = [fn(x) for x in x_vals]
	axes.set_xlim(-10, 10)
	axes.set_ylim(-10, 10)
	axes.plot(x_vals, y_vals)


def plot_circle(obj, axes, **kwargs):
	circ = obj
	
	theta = np.linspace(0, 2*np.pi, 100)
	
	x = circ.radius * np.cos(theta) + circ.center.x
	y = circ.radius * np.sin(theta) + circ.center.y
	
	axes.plot(x, y, color="blue", linewidth=.7)


def plot_polygon(obj, axes, **kwargs):
	plot_segments(obj.sides, axes, **kwargs)
	
def plot(obj, axes=None, **kwargs):
	if axes == None:
		axes = get_default_axes()
	plotter = get_plotter(obj)
	if not plotter:
		print("Warning, unsupported type:", str(type(obj)))
		return axes
	else:
		plotter(obj, axes, **kwargs)
	return axes

def make_plottable(p1, p2):
	# converts ("flattens") two points to two arrays with x-value, y-value
	return [p1.x, p2.x],[p1.y, p2.y]

def plot_segments(segments, axes, **kwargs):
	for s in segments:
		x,y = make_plottable(*s.points)
		axes.plot(x, y, **kwargs)

def test_sympy_expression():
	import sympy as sp
	
	x = sp.symbols('x')
	f = x**3 - x/2
	ax = plot(f)
	print("plot_expression successfully returned a(n)", type(ax))
	