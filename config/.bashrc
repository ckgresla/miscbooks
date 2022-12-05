# CKG's definitive BASHRC config updates (need set if on a remote)


# Default Editor
export VISUAL=/usr/bin/vim
export EDITOR=/usr/bin/vim

# Aliases
alias gcs='git status'
alias rng='ranger' #can install on ubuntu with `sudo apt install ranger`
alias ca='conda activate'
alias ced='conda deactivate'

#vim mode
set -o vi

# Clear Screen Keyboard Shortcut (Ctrl+L)
bind -x '"\C-l":clear'




