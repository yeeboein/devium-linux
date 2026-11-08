# ~/.bashrc - Devium
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias ll='ls -lah'
alias update='devium-update-manager'

# Beginner / Pro mode (change it in the Devium Welcome app or with: devium-mode pro)
DEVIUM_MODE="$(cat ~/.config/devium/mode 2>/dev/null || echo beginner)"

if [[ $DEVIUM_MODE == pro ]]; then
    alias gs='git status' ga='git add' gc='git commit' gp='git push' gl='git log --oneline --graph -20'
    alias py='python' venv='python -m venv .venv && source .venv/bin/activate'
    alias ..='cd ..' ...='cd ../..'
    command -v starship >/dev/null && eval "$(starship init bash)"
else
    PS1='\[\e[1;36m\]\u@\h\[\e[0m\] \[\e[1;35m\]\w\[\e[0m\] \$ '
fi

# Show the Devium logo once per terminal window.
if [[ -z ${DEVIUM_FETCHED:-} ]] && command -v fastfetch >/dev/null; then
    export DEVIUM_FETCHED=1
    fastfetch
    [[ $DEVIUM_MODE != pro ]] && echo -e "  \e[2mTip: type \e[0;36mupdate\e[0;2m to update, or open \e[0;36mDevium Welcome\e[0;2m from the menu for help.\e[0m\n"
fi
