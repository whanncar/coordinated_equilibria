
import NFG
from NFG import NFG

import LP
from LP import prepare_LP_data, get_all_vertices


def get_coord_eq_set(game):
	LP_data = prepare_LP_data(game, game.actions)
	vertices = get_all_vertices(LP_data['matrix'])
	LP_data['vertices'] = vertices
	return LP_data
