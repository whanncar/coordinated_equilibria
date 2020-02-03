
import LP_wrapper


def run_LP(objective, lp_matrix):
	# Make zero vector
	zeros = []
	d = len(lp_matrix)
	for i in range(d):
		zeros.append(0)
	# Run LP
	return LP_wrapper.max_dist_lp_container(objective, lp_matrix, zeros, [], [])
