

all: mv_out_and_kill_folders

mv_out_and_kill_folders:
	mv */*.py .
	rm -r */


clean:
	rm *.pyc -f
	mkdir basic_objects; mv NFG.py threat_function.py unplan.py basic_objects
	mkdir helpers; mv utils.py unutils.py helpers
	mkdir io_ui; mv file_io.py game_editor.py io_ui
	mkdir LP; mv unLP.py LP_wrapper.py LP
	mkdir tests; mv *.py tests
	
