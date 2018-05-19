ClerkBot
========

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

    clerkbot -h

Some actions have further explanation, below.

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
Smith, John: jonsdad@gmail.com, jonsmom@gmail.com

```

Docker
------

To build an image tagged "clerkbot-img", in the project root run:

```bash
docker build -t clerkbot-img .
```

To run clerkbot in a new container:

```bash
docker run -t --rm -v ~/clerkbot/conf:/conf -v ~/clerkbot/output:/output \
    -e "LDS_USERNAME=myusername" -e "LDS_PASSWORD=mypassword" \
    --name clerkbot-cont clerkbot-img clerkbot --records
```

To use a pre-built container, look for genericmoniker/clerkbot on DockerHub.

Project Notes
-------------

* Written for Python 3.
* Requirements are managed with pip-tools.
