
import l_utils
from l_utils import *

import m_utils
from m_utils import *

import unplan

import copy

import threat_function





def get_all_unplans(game):
	# Retrieve states
	states = game.states
	# Retrieve player permutations
	perms = get_all_player_permutations(game)
	# Retrive action profiles
	aps = get_all_action_profiles(game)
	# Make unplans
	unplans = []
	for i in range(len(states)):
		theta = states[i]
		for j in range(len(perms)):
			pi = perms[j]
			for k in range(len(aps)):
				ap = aps[k]
				unplans.append(unplan.Unplan(pi, ap, theta))
	# Return unplans
	return unplans



def make_threat_function(game):
	result = threat_function.ThreatFunction()
	# Attach game to object and set new actions
	result.game = copy.deepcopy(game)
	# Make copy of player list
	players_copy = []
	for i in range(len(result.game.players)):
		players_copy.append(result.game.players[i])
	# Make skeleton to hold data
	result.data = {}
	for i in range(len(result.game.states)):
		result.data[result.game.states[i]] = result.make_skeleton([], players_copy)
	# Populate data with actual values
	result.populate_data()
	return result



def populate_local_threat_functions(unplans, game, tf):
	# Populate
	for u in unplans:
		u.populate_local_threat_function(game, tf)

def get_LP_matrix(unplans, game):
	# Instantiate matrix
	matrix = []
	# Add all columns to matrix as rows
	for i in range(len(unplans)):
		matrix.append(unplans[i].get_LP_column(game))
	# Take transpose of matrix
	matrix = get_transpose(matrix)
	# Return matrix
	return matrix


def get_self_contained_action_set(game):
	# DEFINE tolerance
	tolerance = .000001
	# Make a copy of game whose action set can be changed
	game_copy = copy.deepcopy(game)
	# Set old actions to empty
	old_actions = {}
	# Set new actions to all actions
	new_actions = game.actions
	# Make a copyable empty action set
	empty_action = {}
	for p in game.players:
		empty_action[p] = []
	# While actions are removed
	while old_actions != new_actions:
		# Store new actions to old actions
		old_actions = new_actions
		# Set actions for game to new actions
		game_copy.actions = new_actions
		# Set new actions to empty action set
		new_actions = copy.deepcopy(empty_action)
		# Get unplans
		unplans = get_all_unplans(game_copy)
		# Populate local threat functions for unplans
		populate_local_threat_functions(unplans, game_copy, make_threat_function(game_copy))
		# Get LP matrix
		LP_matrix = get_LP_matrix(unplans, game_copy)
		# Get action indicators
		action_indicators = get_action_indicators(game_copy, unplans)
		# Get maximum probabilities for actions
		action_max_probs = {}
		for p in game.players:
			action_max_probs[p] = {}
			for a in game.actions[p]:
				action_max_probs[p][a] = lp(action_indicators[p][a], LP_matrix)['value']
		# Populate new actions
		for p in game.players:
			for a in game.actions[p]:
				if action_max_probs[p][a] > tolerance:
					new_actions[p].append(a)
	# Return self contained action set
	return new_actions





