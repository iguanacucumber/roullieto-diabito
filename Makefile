serve:
	python3 src/server.py

client:
	python3 src/client.py

watch:
	clear
	tail -f ~/.local/share/online-pacman/db.csv
