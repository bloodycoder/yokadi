" Vim syntax file
" Language: Yokadi t_medit
" Maintainer: Aurélien Gâteau <mail@agateau.com>
" Filenames: *.medit

if exists("b:current_syntax")
  finish
endif

syn case match

syn match yokadimeditComment "^\s*#.*$" skipwhite
syn match yokadimeditTaskId "\v^\s*(\d+|-)" nextgroup=yokadimeditStatus skipwhite
syn match yokadimeditStatus "[NSD]" nextgroup=yokadimeditTitle contained
syn match yokadimeditTitle ".*" contains=yokadimeditKeyword contained
syn match yokadimeditKeyword "@\w\+" contained
syn match yokadimeditKeyword "@\w\+=\d\+" contained

hi def link yokadimeditComment Comment
hi def link yokadimeditTaskId Constant
hi def link yokadimeditStatus Statement
hi def link yokadimeditKeyword Type

let b:current_syntax = "yokadimedit"
