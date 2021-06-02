while true ; do
sleep 5
	cd $HOME/dockerbot
	python3.8 main.py
sleep 5
done
#@reboot tmux new-session -d -s dockerbot "/usr/bin/bash $HOME/dockerbot/auto.sh"
