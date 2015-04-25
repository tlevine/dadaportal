"Set the Message-Id for an email and put a link to the message's
"future location on the Dada Portal.

function! DadaMail()
    let @m=strftime('%Y%m%d.%H%M%S') . '.' . system('printf $RANDOM') . '@' . system('hostname')
    normal gg"mPgg^iMessage-Id: 
    normal G"mp^i---This email is also available here.http://thomaslevine.com/mail/$a/
endfunction

nnoremap m :call DadaMail()<CR>
