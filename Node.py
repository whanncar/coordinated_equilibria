class Node:

  def __init__(self, player, action):
    self.player = player
    self.action = action
    self.children = {} # dict: action -> child corresponding to action

