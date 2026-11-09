# ~/.zshrc - Devium
HISTFILE=~/.zsh_history HISTSIZE=10000 SAVEHIST=10000
setopt autocd interactive_comments hist_ignore_dups share_history
bindkey -e
bindkey '^[[H' beginning-of-line '^[[F' end-of-line '^[[3~' delete-char
bindkey '^[[1;5C' forward-word '^[[1;5D' backward-word

fpath=(/usr/share/zsh/site-functions $fpath)
autoload -Uz compinit && compinit -d ~/.cache/zcompdump
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

alias ls='ls --color=auto' grep='grep --color=auto' ll='ls -lah'
alias update='devium-update-manager'

alias gs='git status' ga='git add' gc='git commit' gp='git push' gl='git log --oneline --graph -20'
alias py='python' venv='python -m venv .venv && source .venv/bin/activate'

if command -v starship >/dev/null; then
    eval "$(starship init zsh)"
else
    PROMPT='%F{cyan}%B%n@%m%b%f %F{magenta}%~%f %# '
fi

# Grey suggestions from your history (press → to accept) and coloured commands.
[[ -f /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && \
    source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
[[ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && \
    source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

if [[ -z ${DEVIUM_FETCHED:-} ]] && command -v fastfetch >/dev/null; then
    export DEVIUM_FETCHED=1
    fastfetch
    print -P "  %F{8}Type %F{cyan}support%F{8} to see helpful commands.%f\n"
fi
