

import scipy
from scipy import optimize


def minimize_container(objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector, list_of_lb_ub_pairs):
	lp_output = optimize.linprog(objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector, list_of_lb_ub_pairs)
	return lp_output


def maximize_container(objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector, list_of_lb_ub_pairs):
	new_objective_vector = []
	for i in range(len(objective_vector)):
		new_objective_vector.append(objective_vector[i] * -1)
	return minimize_container(new_objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector, list_of_lb_ub_pairs)


def maximize_with_probs_container(objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector):
	row_of_ones = []
	for i in range(len(objective_vector)):
		row_of_ones.append(1)
	eq_matrix.append(row_of_ones)
	eq_vector.append(1)
	list_of_lb_ub_pairs = []
	for i in range(len(objective_vector)):
		list_of_lb_ub_pairs.append([0, 1])
	result = maximize_container(objective_vector, ineq_matrix, ineq_vector, eq_matrix, eq_vector, list_of_lb_ub_pairs)
	eq_matrix.pop(-1)
	eq_vector.pop(-1)
	return result



