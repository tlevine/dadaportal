% rebase('base.tpl', title = title)
% if results == None:
<form class="centered-search-bar" action="/+" method="get">
  <input name="q" type="text" />
  <input value="Search" type="submit" />
</form>
% elif len(results) > 0:
<ul class="results">
  % for result in results:
  <li><a href="{{result['href']}}">{{result['title']}}</a></li>
  % end
</ul>
% else:
<em class="results">No results</em>
% end
