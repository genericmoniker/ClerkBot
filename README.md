Clerk
=====

These are a set of utilities potentially helpful for clerks in The 
Church of Jesus Christ of Latter-day Saints.

The scripts generally need your LDS Account credentials. You can either 
set these environment variables, or the scripts will prompt 
interactively:

    LDS_USERNAME
    LDS_PASSWORD

Actions
-------

Actions are invoked from the command line. Try:

    clerk -h

### Missionary Accounts

This action creates emails for missionary accounts to let families of
missionaries know what the current balance is. The emails are created as drafts
in a Gmail account. If the email looks good, you can send it from your drafts
folder.

There are a couple of setup steps needed for this action:

1. You'll need to follow the "Turn on the Gmail API"
instructions at https://developers.google.com/gmail/api/quickstart/python and
save `client_secret.json` in a `conf` directory at the root of the project.
2. Create conf/config.ini to map missionary accounts to email addresses. This
   should look something like this:

```ini
[emails]
Doe, Jane: doefamily@live.com
Smith, John: jonsdad@gmail.com

```


Project Notes
-------------

* Written for Python 3.
* Requirements are managed with pip-tools.
