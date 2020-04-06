
import scipy
from scipy import optimize







### START: Matrix methods

# Get transpose of matrix m
def get_transpose(m):
	result = []
	# Get dimensions of m
	old_num_rows = len(m)
	old_num_cols = len(m[0])
	# Set dimensions of m transpose
	num_rows = old_num_cols
	num_cols = old_num_rows
	# Populate m transpose
	for i in range(num_rows):
		result.append([])
		for j in range(num_cols):
			result[-1].append(m[j][i])
	return result



def make_constant_vector(length, value):
	result = []
	for i in range(length):
		result.append(value)
	return result



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

### END: Matrix methods









### START: List methods

# Get k-tuples of elements of s
def get_ordered_tuples(s, k):

  result = []

  if k == 1:
    for x in s:
      y = []
      y.append(x)
      result.append(y)
    return result

  for x in s:
    smaller = get_ordered_tuples(s, k - 1)
    for y in smaller:
      y.append(x)
      result.append(y)
  return result



# Get list of permutations of given list s
def get_all_permutations(s):
	# Base cases
	if len(s) == 0:
		return []
	if len(s) == 1:
		return [[s[0]]]
	# Other cases
	result = []
	for i in range(len(s)):
		first = s.pop(i)
		subperms = get_all_permutations(s)
		for j in range(len(subperms)):
			result.append([first] + subperms[j])
		s.insert(i, first)
	return result



# Get product of given list s of lists
def get_list_product(s):
	# Base cases
	if len(s) == 0:
		return []
	if len(s) == 1:
		result = []
		for i in range(len(s[0])):
			result.append([s[0][i]])
		return result
	# Other cases
	result = []
	first = s.pop(0)
	subproduct = get_list_product(s)
	for i in range(len(first)):
		for j in range(len(subproduct)):
			point = [first[i]]
			for k in range(len(subproduct[j])):
				point.append(subproduct[j][k])
			result.append(point)
	return result




### END: List methods










### START: LP methods

# Check whether Av >= 0 
def lp_satisfied(v, A):
	# Define tolerance
	tolerance = -.000001
	for i in range(len(A)):
		row = A[i]
		dot = 0
		for j in range(len(row)):
			dot = dot + row[j] * v[j]
		if dot < tolerance:
			return False
	return True



# Maximize c.v
# s.t.     Av >= 0
#          v_i in [0, 1] for all i
#          sum(v_i) = 1
def lp(c, A):
	# Negate c and A to put problem in canonical form
	neg_c = negate_vector(c)
	neg_A = negate_matrix(A)
	# Make column of zeros for -Av <= 0 constraint
	column_of_zeros = make_constant_vector(len(neg_A), 0)
	# Make [0,1] bounds for all v_i
	dim = len(neg_A[0])
	bounds = []
	for i in range(dim):
		bounds.append([0, 1])
	# Make row of ones for sum(v_i) = 1 constraint
	row_of_ones = make_constant_vector(dim, 1)
	# Run LP
	result = package_lp_output(optimize.linprog(neg_c, neg_A, column_of_zeros, [row_of_ones], [1], bounds))
	# Replace -c.v with c.v
	result['value'] = -result['value']
	return result



# Maximize c.v
# s.t.     Av >= 0
#          v_i in [0, 1] for all i
#          sum(v_i) = 1
#          v.1(theta) = pi(theta) for all theta
def lp_with_prior(c, A, pi, state_indicators):
	# Negate c and A to put problem in canonical form
	neg_c = negate_vector(c)
	neg_A = negate_matrix(A)
	# Make column of zeros for -Av <= 0 constraint
	column_of_zeros = make_constant_vector(len(neg_A), 0)
	# Make [0,1] bounds for all v_i
	dim = len(neg_A[0])
	bounds = []
	for i in range(dim):
		bounds.append([0, 1])
	# Make row of ones for sum(v_i) = 1 constraint
	row_of_ones = make_constant_vector(dim, 1)
	# Prepare equality constraints
	B = []
	b = []
	B.append(row_of_ones)
	b.append(1)
	for theta in pi.keys():
		B.append(state_indicators[theta])
		b.append(pi[theta])
	# Run LP
	result = package_lp_output(optimize.linprog(neg_c, neg_A, column_of_zeros, B, b, bounds))
	# Replace -c.v with c.v
	result['value'] = -result['value']
	return result



# Find all extreme points of the convex set defined by
# 
#    Av >= 0
#    v_i in [0, 1] for all i
#    sum(v_i) = 1
def get_vertices(A):
	# Make auxiliary items for preparing H-representation
	dim = len(A[0])
	num_rows = len(A)
	row_of_ones = []
	row_of_minus_ones = []
	for i in range(dim):
		row_of_ones.append(1)
		row_of_minus_ones.append(-1)
	identity = []
	minus_identity = []
	for i in range(dim):
		identity.append([])
		minus_identity.append([])
		for j in range(dim):
			if i == j:
				identity[-1].append(1)
				minus_identity[-1].append(-1)
			else:
				identity[-1].append(0)
				minus_identity[-1].append(0)
	# Make H-representation
	hrep = []
	for i in range(len(A)):
		A_row = A[i]
		hrep.append([])
		hrep[-1].append(0)
		for j in range(len(A_row)):
			hrep[-1].append(A_row[j])
	row_of_ones.insert(0, -1)
	hrep.append(row_of_ones)
	row_of_minus_ones.insert(0, 1)
	hrep.append(row_of_minus_ones)
	for i in range(len(identity)):
		row = identity[i]
		hrep.append([])
		hrep[-1].append(0)
		for j in range(len(row)):
			hrep[-1].append(row[j])
	for i in range(len(minus_identity)):
		row = minus_identity[i]
		hrep.append([])
		hrep[-1].append(1)
		for j in range(len(row)):
			hrep[-1].append(row[j])
	# Make entries into Fractions
	nt = cdd.NumberTypeable('fraction')
	for i in range(len(hrep)):
		for j in range(len(hrep[i])):
			hrep[i][j] = nt.make_number(hrep[i][j])
	# Convert to V-representation 
	# Following example in pyccdlib docs	
	mat = cdd.Matrix(hrep, number_type='fraction')
	mat.rep_type = cdd.RepType.INEQUALITY
	poly = cdd.Polyhedron(mat)
	ext = poly.get_generators()
	result = []
	for i in range(len(ext)):
		result.append([])
		for j in range(1, len(ext[i])):
			result[-1].append(ext[i][j])
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

### END: LP methods




















