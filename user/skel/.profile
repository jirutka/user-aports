# If not running interactively, don't do anything.
[ -z "$PS1" ] && return

# Increase history size.
export HISTSIZE=1000

# Aliases
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias cd..='cd ..'
alias cp='cp -irv'
alias df='df -h'
alias du='du -h -d 1'
alias gl='git lg'
alias l='ls -Ah'
alias ll='ls -Ahl'
alias mv='mv -iv'
alias rm='rm -ir'
alias tailf='tail -f -n 50'
alias tpaste='curl -F "tpaste=<-" https://tpaste.us/'
