

import Tkinter
from Tkinter import *
# import NFG
import sys
import os

def run(filename, game):
	root = Tkinter.Tk()
	root.geometry('600x600')
	app = Window(filename, game, root)
	root.mainloop()


class Window(Frame):

	def __init__(self, filename, game, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	def init_window(self):
		return




if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'No file name provided.'
		exit()
	filename = sys.argv[1]
	game = None
	if filename in os.listdir('.'):
		game = NFG.load(filename)
	run(filename, game)

