(function() {
  var interval = 5 * 1000 // milliseconds
  send('{{ csrf_token }}')
  console.log('{{csrf_token}}')

  function send(csrfmiddlewaretoken) {
    var f = new FormData()
    f.append('hit_id', '{{hit_id}}')
    f.append('csrfmiddlewaretoken', csrfmiddlewaretoken)
    f.append('screen_width', 33)
    f.append('screen_height', 22)

    var r = new XMLHttpRequest();
    r.open('POST', '/track', true)
    r.onreadystatechange = receive
    r.send(f)
  }

  function receive() {
    if (r.readyState==4) {
      setTimeout(function() {send(r.responseText)}, interval)
    }
  }
})()
