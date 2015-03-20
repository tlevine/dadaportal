% rebase('base.tpl', title = title)
    % if body != None:
    % message = threads[0][0]
    <div class="heading">
      <h3>{{message['subject']}}</h3>
      <p>From <a href="/!/{{message['from']}}/">{{message['from']}}</a></p>
      <p>To <a href="/!/{{message['to']}}/">{{message['to']}}</a></p>
      <p>
        {{message['weekday']}},
        <a href="/!/date:{{message['notmuchmonth']}}..{{message['notmuchmonth']}}/">{{message['month']}}</a>
        <a href="/!/date:{{message['notmuchday']}}..{{message['notmuchday']}}/">{{message['day']}}</a>,
        {{message['year']}},
        at {{message['time']}}
      </p>
      <br/>
      <p><a href="{{message['mailto']}}" target="_blank">Reply to this message</a></p>
    </div>
    <article class="body">{{body}}</article>
    <div class="attachments">
      <h3>Attachments</h3>
      <ol>
      % for n, description in parts:
        <li><a href="{{n}}">{{description}}</a></li>
      % end
      </ol>
    </div>
    % end

    <div class="threads">
      % if body != None:
      <h3>Thread</h3>
      % end
      <ul>
        % for thread in threads:
          <ul>
          % for message in thread:
          % include('subthread.tpl', message = message)
          % end
          </ul>
        % end
      </ul>
      % if len(threads) == 100:
      <emph>Only the first 100 threads are displayed.</emph>
      % end
    </div>
