<html>
  <head>
    <title>{{title}}</title>
    <link rel="stylesheet" href="/style.css" type="text/css" />
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/+/date:yesterday../">Recent</a></li>
      </ul>
      <form action="/+" method="get">
        <input name="q" type="text" />
        <input value="Search" type="submit" />
      </form>
    </nav>
    {{!base}}
  </body>
</html>
