
import cdd
import LP_wrapper
import unLP

def run_LP(objective, lp_matrix):
	# Make zero vector
	zeros = []
	d = len(lp_matrix)
	for i in range(d):
		zeros.append(0)
	# Run LP
	return LP_wrapper.max_dist_lp_container(objective, lp_matrix, zeros, [], [])





def get_supported_actions(game):
	# Get unplans and LP matrix
	LP_data = unLP.prepare_LP_data(game)
	unplans = LP_data[0]
	LP_matrix = LP_data[1]
	# Get action indicators
	action_indicators = unLP.get_action_indicators(game, unplans)
	# Calculate supported actions
	result = {}
	players = game.players
	actions = game.actions
	for p in players:
		result[p] = []
		for a in actions[p]:
			max_prob_for_a = run_LP(action_indicators[p][a], LP_matrix)
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
		restricted_game = game.get_copy_with_new_actions(new_actions)
		current_actions = new_actions
		new_actions = get_supported_actions(restricted_game)
	return current_actions




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
	nt = cdd.NumberTypable('fraction')
	for i in range(len(hrep)):
		for j in range(len(hrep[i])):
			hrep[i][j] = nt.make_number(hrep[i][j])
	# Convert to V-representation NOTE: EVERYTHING MUST BE IN FRACTION FORM AT THE MOMENT AND RESULT IS IN FRACTION FORM
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













