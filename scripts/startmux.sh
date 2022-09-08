#!/bin/bash
# Startup Script to get Tmux Working and looking pretty


tmux new-session -d -s General # start session with 1st window
tmux send-keys -t General 'tmux set status-style "bg=default"' Enter''
tmux send-keys -t General 'clear' Enter''

tmux new-session -d -s  ssh #add ssh session
tmux send-keys -t ssh 'tmux set status-style "bg=#2942ff"' Enter'' #make bg of statusbar a nice blue
tmux send-keys -t ssh 'clear' Enter''


tmux attach-session -d -t General #time to rock


