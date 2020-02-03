
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
