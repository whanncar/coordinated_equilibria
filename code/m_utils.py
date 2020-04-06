

import l_utils

from l_utils import *


### START: List methods


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







### START: LP preparation methods




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



