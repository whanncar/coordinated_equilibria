

import utils
import unutils
import unplan
import threat_function

def prepare_LP_data(game):
	unplans = []
	lp_matrix_transpose = []
	# Prepare threat function
	tf = threat_function.ThreatFunction(game)
	# Grab states
	states = game.states
	# Get list of permutations
	perms = unutils.get_all_player_permutations(game)
	# Get list of action profiles
	aps = unutils.get_all_action_profiles(game)
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
	lp_matrix = utils.get_transpose(lp_matrix_transpose)
	# Package unplans and LP matrix together and return
	result = [unplans, lp_matrix]
	return result
