
import NFG
from NFG import NFG

import LP
from LP import prepare_LP_data, get_all_vertices


def get_self_contained_set(game):
	C = get_self_contained_labels(game)
	LP_data = prepare_LP_data(game, C)
	vertices = get_all_vertices(LP_data['matrix'])
	LP_data['vertices'] = vertices
	return LP_data






def get_self_contained_labels(game):
	# Instantiate labels
	# Set new_labels to actions
	# Set different to true
	# While different
		# Set different to false
		# Set labels to new_labels
		# Get LP for labels
		# Populate new_labels with all labels that get positive probability
		# If labels is same as new_labels
			# Set different to false
	# Return labels
