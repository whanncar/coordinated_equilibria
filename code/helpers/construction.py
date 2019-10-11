
import utils
import NFG
import Node
import Plan

from NFG import NFG
from Node import Node
from Plan import Plan



def make_plans_with_given_labels(game, labels): # labels: dict: player -> list of allowed labels
	result = []
	for s in game.states:
		result = result + make_plans_for_given_state(game.actions, s, labels)
	return result




def make_plans_for_given_state_with_given_labels(actions, state, labels):

	if len(actions.keys()) == 1:
		k = actions.keys()[0]
		a = labels[k]
		leaves = []
		for i in a:
			leaves.append(Plan(state, Node(k, i)))
		return leaves

	plans = []

	for k in actions.keys():

		acts = {}
		labs = {}

		for l in actions.keys():
			if l != k:
				acts[l] = []
				labs[l] = []
				for x in actions[l]:
					acts[l].append(x)
				for x in labels[l]:
					labs[l].append(x)
		sp = make_plans_for_given_state_with_given_labels(acts, state, labs)

		for rec in labels[k]:
			ord_tup = utils.get_ordered_tuples(sp, len(actions[k]))
			for tup in ord_tup:
				r = Node(k, rec)
				for i in range(len(tup)):
					r.children[actions[k][i]] = tup[i].get_copy().root
				p = Plan(state, r)
				plans.append(p)

	return plans

