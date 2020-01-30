

import utils


def get_all_player_permutations(game):
	players = game.players
	players_copy = []
	for i in range(len(players)):
		players_copy.append(players[i])
	return utils.get_all_permutations(players_copy)


def get_all_action_profiles(game):
	players = game.players
	actions = []
	# Get list of action lists for players
	for i in range(players):
		actions.append([])
		actions_for_i = game.actions[players[i]]
		for j in range(len(actions_for_i)):
			actions[-1].append(actions_for_i[j])
	# Get product of action lists
	pre_aps = utils.get_list_product(actions)
	# Turn ap lists into ap dictionaries
	result = []
	for i in range(len(pre_aps)):
		ap_list = pre_aps[i]
		ap_dict = {}
		for j in range(len(players)):
			ap_dict[players[j]] = ap_list[j]
		result.append(ap_dict)
	return result


