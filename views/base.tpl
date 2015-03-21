<html>
  <head>
    <title>Dada Portal | {{get('title', 'Thomas Levine')}}</title>
    <link rel="stylesheet" href="/style.css" type="text/css" />
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/+?q=date:yesterday..">Recent</a></li>
      </ul>
      <form action="/+" method="get">
        <input name="q" type="text" value="{{get('q', '')}}" />
        <input value="Search" type="submit" />
      </form>
    </nav>
    {{!base}}
  </body>
</html>
