% rebase('base.tpl', title = title)
% if results == None:
<p>
  % if get('error404', False):
  That page has moved; try searching.
  % else:
  Search the dada.
  % end
  Search bar is at the top-right of the screen.
</p>
% elif len(results) > 0:
<ul class="results">
  % for result in results:
  <li><a href="{{result['href']}}">{{result['title']}}</a></li>
  % end
</ul>
% if len(results) == 100:
<em>Only the first 100 results are displayed; refine your search to see more results.</em>
% end
% else:
<em class="results">No results</em>
% end
