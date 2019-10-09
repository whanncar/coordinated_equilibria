class NFG:

  def __init__(self, players, actions, states, payoffs):
    self.players = players
    self.actions = actions # dict: player -> list of actions
    self.states = states
    self.payoffs = payoffs # nested dict: state -> action of player 1 -> ... -> action of player n -> dict from players to payoffs

  def get_payoffs(self, ap, state):
    result = self.payoffs
    result = result[state]
    for i in range(len(self.players)):
      result = result[ap[self.players[i]]]
    return result

