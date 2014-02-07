tests:
	cd reversi && python tests.py

.ONESHELL:
ci:
	while true; do
		clear
		python tests.py
		inotifywait -q -e create,modify,delete *.py
	done
