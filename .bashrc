export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced
export PS1="\[\e[0;35m\]\u\[\e[0;35m\]:\[\e[0;36m\]\w \[\e[0;37m\]$ \[\e[m\]"
export LS_OPTIONS=--color=auto

alias grep='grep --colour'
alias ll='ls -l'
alias ls='ls -G'
alias me='ifconfig en0'
alias pstack='echo '\''thread backtrace all'\'' | lldb -p'
alias pyperf='python -m cProfile -s tottime'
alias rscp='rsync -v -P -e ssh'
