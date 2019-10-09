
import Node
from Node import Node


class Plan:

  def __init__(self, state, root):
    self.state = state
    self.root = root



  def get_on_path_action_profile(self):
    current = self.root
    ap = {}
    while True:
      ap[current.player] = current.action
      if len(current.children.keys()) == 0:
        break
      current = current.children[current.action]
    return ap



  def get_copy(self):

    r = self.root
    n = Node(r.player, r.action)
    p = Plan(self.state, n)

    if len(r.children.keys()) == 0:
      return p

    for a in r.children.keys():
      sp = Plan(self.state, r.children[a])
      sp = sp.get_copy()
      n.children[a] = sp.root

    return p

