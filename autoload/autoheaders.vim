" Title: Auto-Headers
" Description: A plugin to automatically update your headers.
" Last Change: 4 April 2022
" Maintainer: Kyle L. Davis <AceofSpades5757.github@gmail.com>


"let g:autoheaders_date_format = '%B %d, %Y'
let s:date_format = '%B %d, %Y'


"silent! command! autoheaders#AutoUpdateHeader :call autoheaders#AutoUpdateHeader()
silent! function! autoheaders#AutoUpdateHeader() abort

  " Save Cursor Position
  let start_cursor = getcurpos()[1:-2]


  py3 from autoupdate_headers import Header
  py3 content = '\n'.join(vim.current.buffer[:])
  " Return if buffer is empty
  if !len(py3eval('content'))
    return
  endif
  py3 header = Header(content)

  let s:author = g:snips_author
  let modified = py3eval('header["Modified"]')
  let today = strftime(s:date_format)
  if modified == today
    " Modified Today - Do not update
    call cursor(start_cursor)
    return
  elseif modified == v:null || (has('vim') && modified == v:none)
    call cursor(start_cursor)
    return
  endif

  "py3 header['Author'] = vim.eval('author')
  py3 header['Version'] = header.increment_version()
  py3 header['Modified'] = vim.eval('today')

  py3 start = header.range[0]
  py3 end = header.range[1] - 1
  py3 vim.current.buffer[start:end] = header.lines

  call cursor(start_cursor)
endfunction
