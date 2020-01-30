

all: mv_out_and_kill_folders

mv_out_and_kill_folders:
	mv */*.py .
	rm -r */


clean:
	rm *.pyc -f
	mkdir basic_objects; mv NFG.py Node.py Plan.py threat_function.py unplan.py basic_objects
	mkdir equilibrium_set_calculators; mv coord_eq.py pbe.py self_contained.py equilibrium_set_calculators
	mkdir helpers; mv construction.py utils.py unutils.py helpers
	mkdir io_ui; mv file_io.py game_editor.py io_ui
	mkdir LP; mv LP.py LP_wrapper.py unLP.py LP
	mkdir tests; mv *.py tests
	
