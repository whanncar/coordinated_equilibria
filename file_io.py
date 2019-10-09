
import json

import NFG
from NFG import NFG



def load_NFG(filename):
  f = open(filename, 'r')
  x = json.loads(f.read())
  f.close()
  return NFG(x['players'], x['actions'], x['states'], x['payoffs'])

def save_NFG(g, filename):
  d = {}
  d['players'] = g.players
  d['actions'] = g.actions
  d['states'] = g.states
  d['payoffs'] = g.payoffs
  f = open(filename, 'w')
  f.write(json.dumps(d))
  f.close()

