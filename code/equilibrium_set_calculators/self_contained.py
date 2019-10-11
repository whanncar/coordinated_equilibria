
import NFG
from NFG import NFG

import LP
from LP import prepare_LP_data, get_recommended_action_indicators, get_all_vertices

import LP_wrapper
from LP_wrapper import maximize


def get_self_contained_set(game):
	C = get_self_contained_labels(game)
	LP_data = prepare_LP_data(game, C)
	vertices = get_all_vertices(LP_data['matrix'])
	LP_data['vertices'] = vertices
	return LP_data






def get_self_contained_labels(game):
	# Instantiate labels
	labels = {}
	# Set new_labels to actions
	new_labels = {}
	for player in game.players:
		new_labels[player] = []
		for action in game.actions[player]:
			new_labels[player].append(action)
	# Set different to true
	different = True
	# While different
	while different
		# Set labels to new_labels
		labels = {}
		for player in game.players:
			labels[player] = []
			for action in new_labels[player]:
				labels[player].append(action)
		# Get LP for labels
		LP_data = prepare_LP_data(game, labels)
		# Populate new_labels with all labels that get positive probability
		new_labels = {}
		for player in game.players:
			new_labels[player] = []
		indicators = get_recommended_action_indicators(game, LP_data['obedient profiles'])
		for player in game.players:
			for action in labels[player]:
				lp_output = maximize(indicators[player][action], LP_data['matrix'])
				if lp_output.fun > .000001:
					new_labels[player].append(action)
		# Check whether new_labels is different from labels
		different = False
		for player in game.players:
			if len(labels[player]) != len(new_labels[player]):
				different = True
				break
	# Return labels
	return labels
