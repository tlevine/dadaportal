(function() {
  var interval = 10000 // ten seconds
  send('{{ csrf_token }}')

  function send(csrfmiddlewaretoken) {
    var f = new FormData()
    f.append('hit_id', '{{hit_id}}')
    f.append('csrfmiddlewaretoken', csrfmiddlewaretoken)

    f.append('availWidth', window.screen.availWidth)
    f.append('availHeight', window.screen.availHeight)
    f.append('scrollMaxX', window.scrollMaxX)
    f.append('scrollMaxY', window.scrollMaxY)
    f.append('pageXOffset', window.pageXOffset)
    f.append('pageYOffset', window.pageYOffset)

    var r = new XMLHttpRequest();
    r.open('POST', '{% url "tracking/followup-xhr" %}', true)
    r.onreadystatechange = receive
    r.send(f)

    function receive() {
      if (r.readyState==4 && r.status == 200) {
        function recurse() {
          send(r.responseText.trim())
        }
        setTimeout(recurse, interval)
      }
    }
  }
})()
