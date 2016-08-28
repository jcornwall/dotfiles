set background=dark
set expandtab
set linebreak
set nohlsearch
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

" Reset highlighted search terms on return.
nnoremap  <CR>        :nohlsearch<CR>/<BS><CR>

" Configure key bindings.
inoremap  jk          <Esc>
map!      <S-Insert>  <MiddleMouse>
nmap      t           :tabnew<Space>

" Restore the cursor to the last known position when opening a file.
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

" Enable true color support for theming.
let $NVIM_TUI_ENABLE_TRUE_COLOR=1
