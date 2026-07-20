# When a member of group wheel runs a root shell using sudo or doas and uses
# git, use name and email from his/her .gitconfig.

[ -f /usr/bin/git ] || return

if [ "$USER" = root ]; then
	if [ "$SUDO_GIT_NAME" ] && [ "$SUDO_GIT_EMAIL" ]; then
		git() { /usr/bin/git -c user.name="$SUDO_GIT_NAME" -c user.email="$SUDO_GIT_EMAIL" "$@"; }
	fi

# If $USER is a member of group wheel.
elif id -nG | grep -qw wheel; then
	if [ -z "$SUDO_GIT_NAME" ]; then
		SUDO_GIT_NAME=$(GIT_CONFIG="$HOME/.gitconfig" \
			/usr/bin/git config user.name 2>/dev/null || echo "$USER")
		export SUDO_GIT_NAME
	fi

	if [ -z "$SUDO_GIT_EMAIL" ]; then
		SUDO_GIT_EMAIL=$(GIT_CONFIG="$HOME/.gitconfig" \
			/usr/bin/git config user.email 2>/dev/null || echo "$USER@localhost")
		export SUDO_GIT_EMAIL
	fi
fi
