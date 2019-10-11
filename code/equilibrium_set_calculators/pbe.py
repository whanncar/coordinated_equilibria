
import NFG
from NFG import NFG

import LP
from LP import prepare_LP_data, get_all_vertices

import construction
from construction import make_plans_with_given_labels

def get_pbe_set(game):
	D = get_pbe_labels(game)
	LP_data = prepare_LP_data(game, D)
	vertices = get_all_vertices(LP_data['matrix'])
	LP_data['vertices'] = vertices
	return LP_data



def get_pbe_labels(game):
	# Set labels to actions
	labels = {}
	for player in game.players:
		labels[player] = []
		for action in game.actions[player]:
			labels[player].append(action)
	different = True
  # While labels changes
	while different:
    # Set new_labels to empty set
		new_labels = {}
		changed = True
    # While new_labels changes
		while changed:
			plans = make_plans_with_given_labels(game, labels)
			new_labels_plus_one = get_new_labels_hor(game, plans, labels, new_labels)
			changed = False
			for player in game.players:
				if len(new_labels[player]) != len(new_labels_plus_one[player]):
					changed = True
					new_labels[player] = new_labels_plus_one[player]
	different = False
	for player in game.players:
		if len(labels[player]) != len(new_labels[player]):
			different = True
			labels[player] = new_labels[player]
  # Return labels
	return labels







def get_new_labels_hor(game, plans, base_labels, pred_labels):
	# Initialize result
	result = {}
	for player in game.players:
		result[player] = []
	# Initialize indicator functions
	indicators = {}
	for player in game.players:
		indicators[player] = {}
		for action in base_labels[player]:
			indicators[player][action] = []
	# Make remaining_labels
	remaining_labels = {}
	for player in game.players:
		remaining_labels[player] = []
		for action in base_labels[player]:
			if action not in pred_labels[player]:
				remaining_labels[player].append(action)
	# Initialize matrix
	matrix = []
	for player in game.players:
		for a in remaining_labels[player]:
			for b in game.actions[player]:
				matrix.append([])
	# For each plan
	for plan in plans:
		# Make and add rows for all marked versions of plan and populate indicator functions
		add_deviant_info(game, matrix, indicators, pred_labels, remaining_labels, plan.state, plan.root, {})
	# For each player
	for player in game.players:
		# For each action in base_labels
		for action in base_labels[player]:
			lp_output = maximize(indicators[player][action], matrix)
			if lp_output.fun > .000001:
				result[player].append(action)
	# Return result
	return result






def add_deviant_info(game, matrix, indicators, labels, pred_labels, remaining_labels, state, vertex, pred_ap):
	# Get on path action profile
	# Update indicator functions
	# Get deviation payoffs for each on path vertex
	# Set row to 0
	# For each player
		# For each action a in remaining_labels
			# For each action b available to the player
				# If a is recommended
					# Append difference in payoffs to row
				# Otherwise
					# Append 0 to row
				# Increment row
	# If recommended action for this vertex is in pred_labels
		# For each child vertex
			# Add appropriate action to pred_ap
			# Add deviant info for child vertex
			# Remove added action










