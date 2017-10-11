#!/bin/sh

# If not running interactively, do nothing.
[ -n "$PS1" ] || return

# If not connected via SSH, do nothing.
[ -n "$SSH_CONNECTION" ] || return

# If root, do nothing.
[ "$USER" != root ] || return

# If $USER is not member of wheel, do nothing.
id -nG | grep -qw wheel || return

printf '\033[37;1mLast changes in /etc:\033[0m\n'

git -C /etc log \
	--abbrev-commit \
	--decorate \
	--date=short \
	--format=format:'* %ad: %s  %C(dim white)<%an>%C(reset)' \
	-3

logged=$(ps -o args \
	| sed -En 's/^sshd: (\w+) \[priv\].*/\1/p' \
	| sort | uniq \
	| grep -xv "$USER" \
	| xargs)

if [ -n "$logged" ]; then
	printf "\n\033[37;1mLogged users:\033[0m $logged\n"
fi
