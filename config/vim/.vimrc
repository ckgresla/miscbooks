"CKG's Vimrc"

set ts=4 sw=4

syntax on " Syntax highlighting
set showmatch " Shows matching brackets
set ruler " Always shows location in file (line#)
set smarttab " Autotabs for certain code
set hlsearch "highlights all occurences of word being searched for (could use "hls" instead of "hlsearch")
set ignorecase "ignore casing on word search (could also use "ic" instead of "ignorecase")
set smartindent "magic to smartly indent files




"colorscheme peachpuff "disgusting on normal (somehow theme didn't set bg correctly before Ventura update)

" Config Catppuccin Colors -- more remappings done in colorscheme file (for highlighted words, etc.)
colorscheme CKG-VimColorScheme
set termguicolors




" Status Bar- https://stackoverflow.com/questions/5375240/a-more-useful-statusline-in-vim

" items in status line (actual values)
set laststatus=2
set statusline=
set statusline+=%7*\[%n]                                  "buffernr
set statusline+=%1*\ %<%F\                                "File+path
set statusline+=%2*\ %y\                                  "FileType
set statusline+=%3*\ %{''.(&fenc!=''?&fenc:&enc).''}      "Encoding
set statusline+=%3*\ %{(&bomb?\",BOM\":\"\")}\            "Encoding2
set statusline+=%4*\ %{&ff}\                              "FileFormat (dos/unix..) 
set statusline+=%5*\ %{&spelllang}\%{HighlightSearch()}\  "Spellanguage & Highlight on?
set statusline+=%8*\ %=\ row:%l/%L\ (%03p%%)\             "Rownumber/total (%)
set statusline+=%9*\ col:%03c\                            "Colnr
set statusline+=%0*\ \ %m%r%w\ %P\ \                      "Modified? Readonly? Top/bot.

"Highlight on for Searching
function! HighlightSearch()
  if &hls
    return 'H'
  else
    return ''
  endif
endfunction

"colors to use in StatusLine
hi User1 guifg=#ffdad8  guibg=#880c0e
hi User2 guifg=#000000  guibg=#F4905C
hi User3 guifg=#292b00  guibg=#f4f597
hi User4 guifg=#112605  guibg=#aefe7B
hi User5 guifg=#051d00  guibg=#7dcc7d
hi User7 guifg=#ffffff  guibg=#880c0e gui=bold
hi User8 guifg=#ffffff  guibg=#5b7fbb
hi User9 guifg=#ffffff  guibg=#810085
hi User0 guifg=#ffffff  guibg=#094afe


" Set ink Syntax Highlighting -- TheSephist's programming lang
au BufNewFile,BufRead *.ink set filetype=ink


" KeyBindings

" shortcut to go to "middle" of a line (as seen in- https://superuser.com/questions/216411/go-to-middle-of-line-in-vim)
map gm :call cursor(0, len(getline('.'))/2)<CR>

" remap ":W" to ":w" -- no more nonsensical saving mishaps
command! W write

" remap ":Q" to ":q" -- no more nonsensical quitting mishaps
command! Q quit
" Autocomplete for Typical Special Characters

" Single Keypress will write out the pair of characters (Ex. [] instead of [ for brackets)
" Double Keypress will write out just the single character (Ex. [ instead of [[ for brackets)
inoremap { {}<left>
inoremap {{ {
inoremap {} {}
inoremap [ []<left>
inoremap [[ [
inoremap [] []
inoremap ( ()<left>
inoremap (( (
inoremap () ()
inoremap " ""<left>
inoremap "" ""
inoremap ' ''<left>
inoremap '' ''




" Plug-Ins 
" currently using vim-plug, see- https://github.com/junegunn/vim-plug
call plug#begin('~/.vim/plugged') "init plugins for use, as per- https://stackoverflow.com/questions/69250609/global-vim-plugin-settings-with-vim-plug


" Goyo- https://github.com/junegunn/goyo.vim
Plug 'junegunn/goyo.vim' "a great tool for writing in Vim

function! s:goyo_enter()
	set linebreak
	set spell spelllang=en_us
endfunction

function! s:goyo_leave()
	set nolinebreak
	set nospell
endfunction

autocmd! User GoyoEnter nested call <SID>goyo_enter() 
autocmd! User GoyoLeave nested call <SID>goyo_leave()

let g:goyo_height="85%"
let g:goyo_width="60%"

call plug#end()
" End PlugIn Section -- need call the end() func to get all loaded in


