set background=dark
set cursorline
set expandtab
set linebreak
set noswapfile
set number
set ruler
set shiftwidth=2
set showtabline=2
set smartindent
set tabstop=2

syntax on
colorscheme base16-tomorrow

" Make cursor navigation aware of visible line-wrap.
map       j           gj
map       k           gk
map       <Down>      gj
imap      <Down>      <C-O>gj
map       <Up>        gk
imap      <Up>        <C-O>gk
map       <Home>      g0
imap      <Home>      <C-O>g0
map       <End>       g$
imap      <End>       <C-O>g$

" Configure key bindings.
let mapleader = ','

nmap      <Leader>w   :w<CR>
nmap      <Leader>m   :w<CR>:Neomake!<CR>
map!      <S-Insert>  <MiddleMouse>

" Clear highlighted search when backspace is pressed.
nnoremap <expr> <BS> v:hlsearch ? ':nohlsearch<CR>' : '<BS>'

" Restore the cursor to the last known position when opening a file.
autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" Enable true color support for theming.
let $NVIM_TUI_ENABLE_TRUE_COLOR=1

" Load plugins.
call plug#begin()

Plug 'neomake/neomake'
Plug 'tpope/vim-vinegar'
"Plug 'Valloric/YouCompleteMe', { 'do': './install.py --clang-completer' }

call plug#end()

" Configure plugins.
let g:neomake_open_list = 2
let g:netrw_liststyle = 3
let g:ycm_global_ycm_extra_conf = '~/.config/nvim/ycm_extra_conf.py'

" Disable per-filetype indent overrides.
filetype plugin indent off
