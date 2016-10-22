set background=dark
set clipboard=unnamedplus
set cursorline
set expandtab
set linebreak
set noshowmode
set noswapfile
set number
set relativenumber
set ruler
set shiftwidth=2
set smartindent
set tabstop=2

syntax on

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
map!      <S-Insert>  <MiddleMouse>

" Clear highlighted search when backspace is pressed.
nnoremap <expr> <BS> v:hlsearch ? ':nohlsearch<CR>' : '<BS>'

" Restore the cursor to the last known position when opening a file.
autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" Enable true color support for theming.
let $NVIM_TUI_ENABLE_TRUE_COLOR=1

" Load plugins.
call plug#begin()

Plug 'tpope/vim-vinegar'
Plug 'vim-airline/vim-airline'

call plug#end()

" Configure plugins.
let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#fnamemod = ':t'
let g:netrw_liststyle = 3

" Disable per-filetype indent overrides.
filetype plugin indent off

" Colorscheme depends on Airline extension.
colorscheme base16-tomorrow
