

import NFG
from NFG import NFG

import file_io
from file_io import load_NFG

import coord_eq
from coord_eq import get_coord_eq_set
import self_contained
from self_contained import get_self_contained_set
import pbe
from pbe import get_pbe_set


def test():
	game = load_NFG('test_game.nfg')
	coord_result = get_coord_eq_set(game)
	self_contained_result = get_self_contained_set(game)
	C = self_contained_result['C']
	pbe_result = get_pbe_set(game)
	D = pbe_result['D']
	print C
	print D





if __name__ == '__main__':
	test()




