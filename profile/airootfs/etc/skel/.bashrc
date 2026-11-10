# ~/.bashrc - Devium
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias ll='ls -lah'
alias update='devium-update-manager'

alias gs='git status' ga='git add' gc='git commit' gp='git push' gl='git log --oneline --graph -20'
alias py='python' venv='python -m venv .venv && source .venv/bin/activate'

if command -v starship >/dev/null; then
    eval "$(starship init bash)"
else
    PS1='\[\e[1;36m\]\u@\h\[\e[0m\] \[\e[1;35m\]\w\[\e[0m\] \$ '
fi

# fastfetch only runs when you type it. The first terminal you ever open shows one short tip.
if [[ ! -e ~/.config/devium/terminal-tip-shown ]]; then
    mkdir -p ~/.config/devium && touch ~/.config/devium/terminal-tip-shown
    echo -e "\e[2mTip: type \e[0;36msupport\e[0;2m for helpful commands, or \e[0;36mfastfetch\e[0;2m to show your system info.\e[0m"
fi
