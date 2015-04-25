function! DadaMail()
    let @m=strftime('%Y%m%d-%H%M%S') . '.' . system('echo $RANDOM') . '@' . system('hostname')
    normal ggiMessage-Id: "mPGo---This email is also available here.http://thomaslevine.com/mail/"mPi/
endfunction
