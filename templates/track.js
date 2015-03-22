(function() {
  var interval = 5 * 1000 // milliseconds
  send('{{ csrf_token }}')

  function send(csrfmiddlewaretoken) {
    var f = new FormData()
    f.append('hit_id', '{{hit_id}}')
    f.append('csrfmiddlewaretoken', csrfmiddlewaretoken)

    f.append('availWidth', window.screen.availWidth)
    f.append('availHeight', window.screen.availHeight)
    f.append('scrollMaxX', window.screen.scrollMaxX)
    f.append('scrollMaxY', window.screen.scrollMaxY)
    f.append('pageXOffset', window.screen.pageXOffset)
    f.append('pageYOffset', window.screen.pageYOffset)

    var r = new XMLHttpRequest();
    r.open('POST', '/track', true)
    r.onreadystatechange = receive
    r.send(f)

    function receive() {
      if (r.readyState==4) {
        setTimeout(function() {send(r.responseText)}, interval)
      }
    }
  }

})()
