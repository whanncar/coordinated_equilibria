
import utils
import NFG
import Node
import Plan


def make_plans(game):
  result = []
  for s in game.states:
    result = result + make_plans_for_given_state(game.actions, s)
  return result




def make_plans_for_given_state(actions, state):

  if len(actions.keys()) == 1:
    k = actions.keys()[0]
    a = actions[k]
    leaves = []
    for i in a:
      leaves.append(Plan(state, Node(k, i)))
    return leaves

  plans = []

  for k in actions.keys():

    acts = {}

    for l in actions.keys():
      if l != k:
        acts[l] = []
        for x in actions[l]:
          acts[l].append(x)
    sp = make_plans(acts, state)

    for rec in actions[k]:
      ord_tup = utils.get_ordered_tuples(sp, len(actions[k]))
      for tup in ord_tup:
        r = Node(k, rec)
        for i in range(len(tup)):
          r.children[actions[k][i]] = tup[i].get_copy().root
          p = Plan(state, r)
          plans.append(p)

  return plans

