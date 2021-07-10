# Reset PATH to ensure that */sbin is before */bin.
# This is needed for /usr/sbin/git to work (see sudo_git_vars.sh).

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
