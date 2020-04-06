
import l_utils

import json

import file_io

import sys

import h_utils

import preprocessed_data_file

import copy

import random

def get_preprocessed_data_file(game):
	# Make all unplans
	unplans = h_utils.get_all_unplans(game)
	# Calculate threat function for every unplan
	tf = h_utils.make_threat_function(game)
	h_utils.populate_local_threat_functions(unplans, game, tf)
	# Make CE matrix
	CE_matrix = h_utils.get_LP_matrix(unplans, game)

	# Calculate self contained labels
#	self_contained_actions = h_utils.get_self_contained_action_set(game)
	# Make copy of game with only self contained labels for actions
#	self_contained_game = copy.deepcopy(game)
#	self_contained_game.actions = copy.deepcopy(self_contained_actions)
	# Make all self contained unplans
#	self_contained_unplans = h_utils.get_all_unplans(self_contained_game)
	# Calculate threat function for every self contained unplan
#	sc_tf = h_utils.make_threat_function(self_contained_game)
#	h_utils.populate_local_threat_functions(self_contained_unplans, self_contained_game, sc_tf)
	# Make self contained matrix
#	sc_matrix = h_utils.get_LP_matrix(self_contained_unplans, self_contained_game)

	dim = len(unplans)

	for i in range(1):
		rand = []
		for j in range(dim):
			rand.append(random.random())
			if random.random() < .5:
				rand[-1] = -rand[-1]
#		l_utils.lp(rand, CE_matrix)

	# Package calculated quantities
	result = preprocessed_data_file.PreprocessedDataFile()
#	result.set_values(unplans, CE_matrix, self_contained_actions, self_contained_unplans, sc_matrix)
	result.set_values(unplans, CE_matrix, [], unplans, [])
	# Return package
	return result



if __name__ == '__main__':
	game_name = sys.argv[1]
	game = file_io.load_NFG(game_name + '.nfg')
	pdf = get_preprocessed_data_file(game)
	zipped_pdf = pdf.zip()
	f = open(game_name + '.data', 'w')
	f.write(json.dumps(zipped_pdf))
	f.close()
