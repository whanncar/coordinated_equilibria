# coordinated_equilibria



## Requirements

The following Python modules are required; please make sure you already have them installed before using:
* json
* python-tk (to use the game editor)
* copy
* pycddlib
* scipy

To test whether you already have these, open Python and run the following import commands:
~~~
>>> import json
>>> import Tkinter
>>> import copy
>>> import cdd
>>> import scipy
~~~
Instructions for easily installing any of these that are missing are readily available online.


## Example



Navigate to the "code" directory and run
~~~
python game_editor.py
~~~
to create a game. For this example, we will use the name "Cournot". After you fill in the details of the game and click "save", the game will be stored in your working directory as "Cournot.nfg".

Now, start Python and import file_io and calculator:
~~~
>>> import file_io, calculator
~~~

Next, load the game and create the calculator instance:
~~~
>>> game = file_io.load_NFG('Cournot.nfg')
>>> calc = calculator.Calculator(game)
~~~

The following methods can then be used to study the game:
~~~
# Get list of unplans
>>> calc.get_unplans()
# Get vertices of set of unequilibria
>>> calc.get_unequilibrium_vertices()
# Get the actions that appear in self contained equilibria
>>> calc.get_self_contained_support()
# Get list of self-contained unplans
>>> calc.get_self_contained_unplans()
# Get vertices of set of self-contained unequilibria
>>> calc.get_self_contained_unequilibrium_vertices()
~~~


## Documentation

To be written










