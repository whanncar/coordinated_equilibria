

import scipy
from scipy import optimize

# Minimize c.v
# s.t.     Av <= a
#          Bv = b
#          lb <= v <= ub
def lp_container(c, A, a, B, b, lb, ub):
	# Put bounds into required form
	bounds = []
	for i in range(len(lb)):
		bounds.append([lb[i], ub[i]])
	# Run LP
	return optimize.linprog(c, A, a, B, b, bounds)


# Minimize c.v
# s.t.     Av <= a
#          Bv = b
#          v_i in [0, 1] for all i
#          sum(v_i) = 1
def dist_lp_container(c, A, a, B, b):
	# Get dimension of space
	dim = len(A[0])
	# Make lb and ub
	lb = []
	ub = []
	for i in range(dim):
		lb.append(0)
		ub.append(1)
	# Add sum(v_i) = 1 constraint
	row_of_ones = []
	for i in range(dim):
		row_of_ones.append(1)
	B.append(row_of_ones)
	b.append(1)
	# Run LP
	return lp_container(c, A, a, B, b, lb, ub)
