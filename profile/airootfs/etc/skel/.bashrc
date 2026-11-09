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

# Show the Devium logo once per terminal window.
if [[ -z ${DEVIUM_FETCHED:-} ]] && command -v fastfetch >/dev/null; then
    export DEVIUM_FETCHED=1
    fastfetch
    echo -e "  \e[2mType \e[0;36msupport\e[0;2m to see helpful commands.\e[0m\n"
fi
