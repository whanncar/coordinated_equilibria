

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
	return package_lp_output(optimize.linprog(c, A, a, B, b, bounds))



# Maximize c.v
# s.t.     Av >= a
#          Bv = b
#          lb <= v <= ub
def max_lp_container(c, A, a, B, b, lb, ub):
	return lp_container(negate_vector(c), negate_matrix(A), negate_vector(a), B, b, lb, ub)






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


# Maximize c.v
# s.t.     Av >= a
#          Bv = b
#          v_i in [0, 1] for all i
#          sum(v_i) = 1
def max_dist_lp_container(c, A, a, B, b):
	return dist_lp_container(negate_vector(c), negate_matrix(A), negate_vector(a), B, b)




### Some helper methods

def negate_vector(v):
	result = []
	for i in range(len(v)):
		result.append(-v[i])
	return result


def negate_matrix(m):
	result = []
	for i in range(len(m)):
		row = m[i]
		neg_row = []
		for j in range(len(row)):
			neg_row.append(-row[j])
		result.append(neg_row)
	return result


def package_lp_output(output):
	value = output.fun
	v = []
	output_v = output.x
	for i in range(len(output_v)):
		v.append(output_v[i])
	result = {}
	result['value'] = value
	result['v'] = v
	return result
