
import copy

import cdd

import scipy
from scipy import optimize

import unplan
import threat_function




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



def get_all_player_permutations(game):
	players = game.players
	players_copy = []
	for i in range(len(players)):
		players_copy.append(players[i])
	return get_all_permutations(players_copy)



def get_all_action_profiles(game):
	players = game.players
	actions = []
	# Get list of action lists for players
	for i in range(len(players)):
		actions.append([])
		actions_for_i = game.actions[players[i]]
		for j in range(len(actions_for_i)):
			actions[-1].append(actions_for_i[j])
	# Get product of action lists
	pre_aps = get_list_product(actions)
	# Turn ap lists into ap dictionaries
	result = []
	for i in range(len(pre_aps)):
		ap_list = pre_aps[i]
		ap_dict = {}
		for j in range(len(players)):
			ap_dict[players[j]] = ap_list[j]
		result.append(ap_dict)
	return result

### END: List methods










### START: LP methods

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










### START: LP preparation methods

def prepare_LP_data(game):
	unplans = []
	lp_matrix_transpose = []
	# Prepare threat function
	tf = threat_function.ThreatFunction(game)
	# Grab states
	states = game.states
	# Get list of permutations
	perms = get_all_player_permutations(game)
	# Get list of action profiles
	aps = get_all_action_profiles(game)
	# Make unplans and transpose of LP matrix
	for i in range(len(states)):
		state = states[i]
		for j in range(len(perms)):
			pi = perms[j]
			for k in range(len(aps)):
				ap = aps[k]
				# Make unplan for this triple
				unplans.append(unplan.Unplan(tf, pi, ap, state))
				# Compute column for this triple and add it to transpose of LP matrix as a row
				lp_matrix_transpose.append(unplans[-1].get_LP_column())
	# Take transpose of transpose of LP matrix to get LP matrix
	lp_matrix = get_transpose(lp_matrix_transpose)
	# Package unplans and LP matrix together and return
	result = [unplans, lp_matrix]
	return result



def prepare_self_contained_LP_data(game):
	new_game = copy.deepcopy(game)
	new_actions = get_self_contained_action_set(game)
	new_game.actions = new_actions
	LP_data = prepare_LP_data(new_game)
	result = {}
	result['actions'] = new_actions
	result['LP'] = LP_data
	return result


def get_action_indicators(game, unplans):
	result = {}
	players = game.players
	actions = game.actions
	# Prepare space for each indicator vector
	for p in players:
		result[p] = {}
		for a in actions[p]:
			result[p][a] = []
	# Populate indicator vectors
	for i in range(len(unplans)):
		ap = unplans[i].ap
		for p in players:
			for a in actions[p]:
				if ap[p] == a:
					result[p][a].append(1)
				else:
					result[p][a].append(0)
	return result



def get_state_indicators(game, unplans):
	result = {}
	states = game.states
	# Prepare space for each indicator vector
	for s in states:
		result[s] = []
	# Populate indicator vectors
	for i in range(len(unplans)):
		s_i = unplans[i].state
		for s in states:
			if s == s_i:
				result[s].append(1)
			else:
				result[s].append(0)
	return result

### END: LP preparation methods










### START: Wrappers

def get_supported_actions(game):
	# Get unplans and LP matrix
	LP_data = prepare_LP_data(game)
	unplans = LP_data[0]
	LP_matrix = LP_data[1]
	# Get action indicators
	action_indicators = get_action_indicators(game, unplans)
	# Calculate supported actions
	result = {}
	players = game.players
	actions = game.actions
	for p in players:
		result[p] = []
		for a in actions[p]:
			max_prob_for_a = lp(action_indicators[p][a], LP_matrix)
			# DEFINING TOLERANCE FOR SUPPORT HERE
			if max_prob_for_a > .000001:
				result[p].append(a)
	return result



def get_self_contained_action_set(game):
	# Set current action set to all actions
	current_actions = game.actions.copy()
	# Calculate supported actions
	new_actions = get_supported_actions(game)
	# Iteratively restrict action set until it stabilizes
	while new_actions != current_actions:
		current_actions = new_actions
		restricted_game = copy.deepcopy(game)
		restricted_game.actions = current_actions
		new_actions = get_supported_actions(restricted_game)
	return current_actions

### END: Wrappers


















