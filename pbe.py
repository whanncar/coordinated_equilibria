
import NFG
from NFG import NFG

import LP
from LP import prepare_LP_data, get_all_vertices


def get_pbe_set(game):
	D = get_pbe_labels(game)
	LP_data = prepare_LP_data(game, D)
	vertices = get_all_vertices(LP_data['matrix'])
	LP_data['vertices'] = vertices
	return LP_data



def get_pbe_labels(game):
	# TODO: everything
