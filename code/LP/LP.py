

import construction


def prepare_LP_data(game, labels):
	# Make plans with given labels
	plans = construction.make_plans_with_given_labels(game, labels)
	# For each plan, get deviation payoffs
	payoffs = []
	for p in plans:
		payoffs.append(p.get_deviation_payoffs(game))
	# For each plan, get on path profiles
	on_path_profiles = []
	for p in plans:
		on_path_profiles.append(p.get_on_path_action_profile())
	# Organize plans into matrix
	matrix = []
	for player in game.players:
		for a in labels[player]:
			for b in game.actions[player]:
				row = []
				for i in range(len(plans)):
					# These variables are defined to make the code a little easier to read
					p = plans[i]
					dev_payoffs = payoffs[i]
					recommendations = on_path_profiles[i]
					# The code really begins here
					if a == recommendations[player]:
						row.append(dev_payoffs[player][b] - dev_payoffs[player][a])
					else:
						row.append(0)
				matrix.append(row)
	result = {}
	result['plans'] = plans
	result['obedient profiles'] = on_path_profiles
	result['matrix'] = matrix
	return result




def get_recommended_action_indicators(game, on_path_profiles):
	num_plans = len(on_path_profiles)
	result = {}
	for player in game.players:
		result[player] = {}
		for action in game.actions[player]:
			result[player][action] = [0] * num_plans
	for i in range(len(on_path_profiles)):
		ap = on_path_profiles[i]
		for player in game.players:
			result[player][ap[player]][i] = 1
	return result



def get_all_vertices(matrix):
	# TODO: Settle on an algorithm

















