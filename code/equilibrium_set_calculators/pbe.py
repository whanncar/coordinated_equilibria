
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
	# Set labels to actions
  # While labels changes
    # Set new_labels to empty set
    # While new_labels changes
      # Get deviant plans with things on new_labels above marked vertex
      # Get distributions which satisfy incentive constraints away from new_labels
      # Get things in support of those distributions and add these to new_labels
    # Set labels to new_labels
  # Return labels
