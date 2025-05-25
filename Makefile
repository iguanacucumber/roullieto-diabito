serve:
	python3 src/server.py

client:
	python3 src/client.py

clean:
	rm -rf ~/.local/share/online-pacman

watch-users:
	clear
	tail -f ~/.local/share/online-pacman/users.csv

watch-lobbies:
	clear
	tail -f ~/.local/share/online-pacman/lobbies.csv
