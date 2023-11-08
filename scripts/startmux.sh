#!/bin/bash
# Startup Script to get Tmux Working and looking pretty


tmux new-session -d -s General # start session with 1st window
tmux send-keys -t General 'tmux rename-window main' Enter''
tmux send-keys -t General 'tmux set status-style "bg=default"' Enter''
tmux send-keys -t General 'tmux rename-window main' Enter''
tmux send-keys -t General 'clear' Enter''

tmux new-session -d -s  ssh #add ssh session
# tmux send-keys -t ssh 'tmux set status-style "bg=#2942ff"' Enter'' #make bg of statusbar a bright blue
# tmux send-keys -t ssh 'tmux set status-style "bg=#7287fd"' Enter'' #catppucin latte - lavender
# tmux send-keys -t ssh 'tmux set status-style "bg=#dd7878"' Enter'' #catppucin latte - flamingo
# tmux send-keys -t ssh 'tmux set status-style "bg=#dc8a78"' Enter'' #catppucin latte - rosewater
tmux send-keys -t ssh 'tmux set status-style "bg=#1e66f5"' Enter'' #catppucin latte - blue

tmux send-keys -t ssh 'clear' Enter''


tmux attach-session -d -t General #time to rock


