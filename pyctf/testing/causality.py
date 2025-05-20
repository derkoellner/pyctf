#! /usr/bin/env python

from numpy import array, zeros, sqrt, log, abs, dot, linalg, hstack

def get_ma(d, p):
	"""Create an order p moving average model for a timeseries. Return a weight
	vector that is of length p and the residual vector of the model."""

	d = d.copy()

	# z-score
	d -= d.mean()
	d /= d.std()

	e = len(d) - p

	# Create a trajectory matrix of dimension e by p.
	# The rows of T are successive windows of the timeseries.
	T = zeros((e, p))
	for i in range(e):
		T[i,:] = d[i:i + p]

	# Using the first p values, predict the p+1st. T[0] * c = d[p]
	# This finds the best solution across the whole timeseries.
	r = linalg.lstsq(T, d[p:p + e])

	# Get the coefficients of a moving average model of order p.
	c = r[0]

	# Compute the residual.
	u = dot(T, c) - d[p:p + e]

	return c, u

def get_ma2(d1, d2, p):
	"""Create an order p moving average model for a pair of timeseries.
	Return a weight vector that is of length 2p and the residual vector."""

	d1 = d1.copy()
	d2 = d2.copy()

	# z-score
	d1 -= d1.mean()
	d1 /= d1.std()
	d2 -= d2.mean()
	d2 /= d2.std()

	# We will try to predict d1[p] from d1 and d2.

	e = len(d1) - p

	# Create a double wide trajectory matrix of dimension e x 2p.
	# The rows of T are successive windows of the timeseries.
	T = zeros((e, p + p))
	for i in range(e):
		T[i,:] = hstack((d1[i:i + p], d2[i:i + p]))

	# Using the first p values, predict the p+1st. T[0] * c = d[p]
	# This finds the best solution across the whole timeseries.
	r = linalg.lstsq(T, d1[p:p + e])

	# Get the coefficients of a moving average model of order 2p.
	c = r[0]

	# Compute the residual.
	u = dot(T, c) - d1[p:p + e]

	return c, u

def causality(d1, d2, order):
	# How much does the prediction of d1 improve when we use d2?
	c, u1 = get_ma(d1, order)
	S1 = dot(u1, u1) / len(u1)
	c, u2 = get_ma2(d1, d2, order)
	S2 = dot(u2, u2) / len(u2)

	# How much does the prediction of d2 improve when we use d1?
	c, v1 = get_ma(d2, order)
	T1 = dot(v1, v1) / len(v1)
	c, v2 = get_ma2(d2, d1, order)
	T2 = dot(v2, v2) / len(v2)

	C = dot(u2, v2) / len(v2)
	Y = array([[S2, C], [C.T, T2]])
	d = sqrt(linalg.det(dot(Y.T, Y)))

	Fyx = log(abs(S1)/abs(S2))
	Fxy = log(abs(T1)/abs(T2))
	Fxdy = log(abs(S2) * abs(T2) / d)
	Fxcy = Fyx + Fxy + Fxdy

	#print 'Fy->x =', Fyx
	#print 'Fx->y =', Fxy
	#print 'Fx.y =', Fxdy
	#print 'Fx,y =', Fxcy

	return (Fyx, Fxy, Fxdy, Fxcy)
