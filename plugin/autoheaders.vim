" Title:       Auto-Headers
" Description: A plugin to automatically update your headers.
" Last Change: 2022 Apr 14
" Maintainer:  Kyle L. Davis <AceofSpades5757.github@gmail.com>


if exists("g:loaded_autoheaders")
    finish
endif
let g:loaded_autoheaders = 1


" User Interface
command! AutoUpdateHeader :call autoheaders#AutoUpdateHeader()
