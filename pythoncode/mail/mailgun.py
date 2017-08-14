def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb9fae69215e94c81944d1572cd74f2b2.mailgun.org/messages",
        auth=("api", "key-f7e5732be7e9c23b23a7f99c7c5cd877"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxb9fae69215e94c81944d1572cd74f2b2.mailgun.org>",
              "to": "wyc <mortimer2015@hotmail.com>",
              "subject": "Hello wyc",
              "text": "Congratulations wyc, you just sent an email with Mailgun!  You are truly awesome!"})