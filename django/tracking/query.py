# success
where status_code = 200

# not bot
where user_agent not similar to '%(Bot|Spider|Baidu|Google|Yahoo)%'

# past week
where datetime_start > '2015-04-09'
