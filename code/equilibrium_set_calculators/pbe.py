
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
	lower_ap = {}
	current = vertex
	while True:
		lower_ap[current.player] = current.action
		if len(current.children.keys()) == 0:
			break
		current = current.children[current.action]
	# Update indicator functions
	for player in game.players:
		for action in base_labels[player]:
			if player not in lower_ap.keys():
				indicators[player][action].append(0)
			elif action != lower_ap[player]:
				indicators[player][action].append(0)
			else:
				indicators[player][action].append(1)
	# Get deviation payoffs for each on path vertex
	payoffs = {}
	current = vertex
	while True:
		payoffs[current.player] = {}
		ap = {}
		for player in pred_ap.keys():
			ap[player] = pred_ap[player]
		for player in lower_ap.keys():
			ap[player] = lower_ap[player]
		for deviant_action in game.actions[current.player]:
			ap[current.player] = deviant_action
			sub_current = current
			while len(sub_current.children.keys()) > 0:
				sub_current = sub_current.children[ap[sub_current.player]]
				ap[sub_current.player] = sub_current.action
			payoffs[current.player][deviant_action] = game.get_payoffs(ap, state)[current.player]
		if len(current.children.keys()) == 0:
			break
		current = current.children[current.action]
	# Set row to 0
	row = 0
	# For each player
	for player in game.players:
		# For each action a in remaining_labels
		for a in remaining_labels[player]:
			# For each action b available to the player
			for b in game.actions[player]:
				# If a is recommended
				if player in payoffs.keys() and lower_ap[player] == a:
					# Append difference in payoffs to row
					matrix[row].append(payoffs[player][b] - payoffs[player][a])
				# Otherwise
				else:
					# Append 0 to row
					matrix[row].append(0)
				# Increment row
				row = row + 1
	# If recommended action for this vertex is in pred_labels
	if len(vertex.children.keys()) == 0:
		return
	if vertex.action in pred_labels[vertex.player]:
		# For each child vertex
		for a in game.actions[vertex.player]:
			# Add appropriate action to pred_ap
			pred_ap[vertex.player] = a
			# Add deviant info for child vertex
			add_deviant_info(game, matrix, indicators, labels, pred_labels, remaining_labels, state, vertex.children[a], pred_ap)
			# Remove added action
			pred_ap.pop[vertex.player]










