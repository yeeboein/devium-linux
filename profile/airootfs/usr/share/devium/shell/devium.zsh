# Devium shell extras (zsh). Sourced from ~/.zshrc.
#  - a notification when a command that took 30+ seconds finishes (builds, installs, tests)
#    change the time: export DEVIUM_NOTIFY_AFTER=60    turn off: export DEVIUM_NOTIFY_AFTER=0
#  - mise (per-project language versions), zoxide (z <folder>) and fzf (Ctrl+R) when installed

# Devium Tools > Coding tools > Build notifications saves the time here
[[ -z ${DEVIUM_NOTIFY_AFTER:-} && -r ${XDG_CONFIG_HOME:-$HOME/.config}/devium/notify-after ]] && \
    DEVIUM_NOTIFY_AFTER=$(< "${XDG_CONFIG_HOME:-$HOME/.config}/devium/notify-after")
: ${DEVIUM_NOTIFY_AFTER:=30}
_devium_skip='^(vim|nvim|vi|nano|micro|kate|code|codium|less|more|man|ssh|htop|btop|top|watch|tmux|screen|python|python3|ipython|node|irb|psql|mysql|sqlite3|lazygit|fzf|cmatrix|asciiquarium|cbonsai|tail -f|journalctl -f|docker logs -f|npm run dev|npm start|yarn dev|pnpm dev|flask run|cargo watch)( |$)'
_devium_preexec() { _devium_cmd="$1"; _devium_start=$EPOCHSECONDS; }
_devium_precmd() {
    local code=$? took
    [[ -z ${_devium_start:-} ]] && return
    took=$(( EPOCHSECONDS - _devium_start )); unset _devium_start
    (( DEVIUM_NOTIFY_AFTER > 0 && took >= DEVIUM_NOTIFY_AFTER )) || return
    [[ $_devium_cmd =~ $_devium_skip ]] && return
    command -v notify-send >/dev/null || return
    local t="$((took / 60))m $((took % 60))s"; (( took < 60 )) && t="${took}s"
    if (( code == 0 )); then
        notify-send --app-name=Terminal --icon=utilities-terminal --expire-time=8000 "Finished ($t)" "${_devium_cmd:0:120}" &!
    else
        notify-send --app-name=Terminal --icon=dialog-error --expire-time=12000 "Failed ($t, code $code)" "${_devium_cmd:0:120}" &!
    fi
}
zmodload zsh/datetime 2>/dev/null
autoload -Uz add-zsh-hook
add-zsh-hook preexec _devium_preexec
add-zsh-hook precmd _devium_precmd

command -v mise >/dev/null && eval "$(mise activate zsh)"
command -v zoxide >/dev/null && eval "$(zoxide init zsh)"
if command -v fzf >/dev/null; then source <(fzf --zsh 2>/dev/null); fi
