
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
	# TODO: everything
