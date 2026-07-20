# This script sets environment variables SUDO_GIT_NAME and SUDO_GIT_EMAIL
# with values from the user's .gitconfig. The variables are used by
# /usr/local/sbin/git wrapper script to pass user's name and email to git
# when executed via sudo root (both sudo git and sudo sh) or doas.

# If root, do nothing.
[ "$USER" != root ] || return

# If $USER is not member of group wheel, do nothing.
id -nG | grep -qw wheel || return

SUDO_GIT_NAME=$(GIT_CONFIG="$HOME/.gitconfig" \
	/usr/bin/git config user.name 2>/dev/null || echo "$USER")
SUDO_GIT_EMAIL=$(GIT_CONFIG="$HOME/.gitconfig" \
	/usr/bin/git config user.email 2>/dev/null || echo "$USER@localhost")

export SUDO_GIT_NAME
export SUDO_GIT_EMAIL
