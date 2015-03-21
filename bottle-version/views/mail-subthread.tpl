<li>
  <a href="/@/id:{{message['message_id']}}">
    % if message['is_match']:
    <strong>
    % end
      {{message['subject']}}
    % if message['is_match']:
    </strong>
    % end
  </a>
</li>
<ul>
  % for reply in message['replies']:
  % include('mail-subthread.tpl', message = reply)
  % end
</ul>
