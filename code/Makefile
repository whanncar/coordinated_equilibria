

all: mv_out_and_kill_folders

mv_out_and_kill_folders:
	mv */*.py .
	rm -r */


clean:
	mkdir basic_objects; mv NFG.py Node.py Plan.py basic_objects
	mkdir equilibrium_set_calculators; mv coord_eq.py pbe.py self_contained.py equilibrium_set_calculators
	mkdir helpers; mv construction.py utils.py helpers
	mkdir io_ui; mv file_io.py io_ui
	mkdir LP; mv LP.py LP_wrapper.py LP
	mkdir tests; mv *.py tests
	
