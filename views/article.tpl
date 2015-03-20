<article>
  <header>
    <h1>Title</h1>
    <em>created at strftime('%B %d, %Y') rescue ''</em>
    <span>tags</span>
  </header>
  <hr/>
  {{!body}}
</article>

<div id="pagination">
    = link_to('View source', 'https://github.com/tlevine/www.thomaslevine.com/tree/master/content' + @item.identifier + 'index.md')
    = if @item[:other_source] then link_to('Other source', @item[:other_source])
    = link_to('Discuss', @item[:tweet_link] || 'https://twitter.com/thomaslevine')
</div>
