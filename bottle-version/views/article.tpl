% rebase('base.tpl', title = title)
<article>
  {{!body}}
</article>

<div id="pagination">
    <em>created at strftime('%B %d, %Y') rescue ''</em>
    = link_to('View source', 'https://github.com/tlevine/www.thomaslevine.com/tree/master/content' + @item.identifier + 'index.md')
    = if @item[:other_source] then link_to('Other source', @item[:other_source])
    = link_to('Discuss', @item[:tweet_link] || 'https://twitter.com/thomaslevine')
</div>