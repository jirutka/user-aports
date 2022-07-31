let s:cachedir = exists("$XDG_CACHE_HOME") ? $XDG_CACHE_HOME : $HOME . '/.cache'
let s:cachedir .= '/vim'

" NOTE: Double trailing slashes // in paths are to include path info in file
"  name (e.g. backup file for /root/foo is saved as %root%foo).

" Save your backups to a less annoying place than the current directory.
" If you have .vim/ in the current directory, it will be used.
" Otherwise it saves it to $XDG_CACHE_HOME/vim/backup/ or ./ if all else fail.
let s:backupdir = s:cachedir . '/backup'
if !isdirectory(s:backupdir)
  silent! call mkdir(s:backupdir, 'p', 0700)
endif
let &backupdir = join(['./.vim/backup/', s:backupdir . '//', '.'], ',')
set backup

" Save your swp files to a less annoying place than the current directory.
" If you have .vim/ in the current directory, it will be used.
" Otherwise it saves it to $XDG_CACHE_HOME/vim/swap/, or ./ if all else fail.
let s:swapdir = s:cachedir . '/swap'
if !isdirectory(s:swapdir)
  silent! call mkdir(s:swapdir, 'p', 0700)
endif
let &directory = join(['./.vim/swap/' , s:swapdir . '//', '.'], ',')

" viminfo stores the the state of your previous editing session
let &viminfo .= ',n' . s:cachedir . '/viminfo'

" This is only present in 7.3+
if exists('+undofile')
  " undofile allows you to use undos after exiting and restarting
  " This, like swap and backups, uses .vim/ first, then $XDG_CACHE_HOME/vim/undo/.
  " :help undo-persistence
  let s:undodir = s:cachedir . '/undo'
  if !isdirectory(s:undodir)
    silent! call mkdir(s:undodir, 'p', 0700)
  endif
  let &undodir = join(['./.vim/undo/', s:undodir . '//'], ',')
  set undofile
endif

" Enable bracketed paste mode.
" http://stackoverflow.com/a/7053522/2217862
if &term =~ 'xterm.*'
  let &t_ti = &t_ti . '\e[?2004h'
  let &t_te = '\e[?2004l' . &t_te
  function XTermPasteBegin(ret)
    set pastetoggle=<Esc>[201~
    set paste
    return a:ret
  endfunction
  map <expr> <Esc>[200~ XTermPasteBegin("i")
  imap <expr> <Esc>[200~ XTermPasteBegin("")
  cmap <Esc>[200~ <nop>
  cmap <Esc>[201~ <nop>
endif
