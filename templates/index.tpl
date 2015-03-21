% rebase('base.tpl')
<div id="head" class="justify">
  <div id="callingcard" class="small card">
    <img alt="Tom's hat" src="img/pink_hat_icon-200.png" />
    <a rel="me" href="">thomas levine</a>
    <a rel="me" href="mailto:_@thomaslevine.com">_@thomaslevine.com</a>
    <blockquote><code>pip install <a href="https://pypi.python.org/pypi/tlevine">tlevine</a> && tlevine</code></blockquote>
    <p>Below are some things I've done, grouped rather arbitrarily into boxes of two to five things. <!--Go <a href="!/jobs">here</a> if you want to hire some computer/dada work.--></p>
  </div>
</div>
<div id="popular" class="justify">
  % for article in popular:
  <div class="popular small card">
    % if article['image'] == None:
    <h2><a href="{{article['endpoint']}}">{{article['title']}}</a></h2>
    <p>{{article['description']}}</p>
    % else
    <a href="{{article['endpoint']}}" title="{{article['title']}}">
      <img src="{{article['image']}}" alt="{{article['title']}}" />
    </a>
    % end
  </div>
  % end
</div>
<div id="foot" class="justify">
  <div id="profiles" class="big card">
    <h2>profiles</h2>
    <ul>
      <li><a href="/!/about/">thomaslevine.com</a>
      <li><a href="http://facebook.com/perluette" rel="me">facebook</a>
      <li><a href="https://twitter.com/thomaslevine" rel="me">twitter</a>
      <li><a href="https://www.linkedin.com/in/tlevine" rel="me">linkedin</a>
      <li><a href="https://plus.google.com/112237825767532686869" rel="me">google</a>
    </ul>
  </div>
</div>
