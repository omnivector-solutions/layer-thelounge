# Lounge IRC
This charm provides Lounge IRC, the self-hosted web IRC client.

# Simple Deploy
1. Deploy the charm!
  ```bash
  juju deploy lounge-irc
  ```
2. Add a user 
  ```bash
  juju run-action lounge-irc/0 add-user name=myname password=mypassword
  ```
3. Login to the webui with the user creds created in #2


# Deploy with reverse proxy
```bash
juju deploy haproxy
juju deploy lounge-irc
juju relate lounge-irc haproxy
```

# User Lifecycle
This charm ships with a few user management lifecycle actions:
```bash
# Add User
juju run-action lounge-irc/0 add-user name=myname password=mypassword

# List Users
juju run-action lounge-irc/0 list-users

# Delete User
juju run-action lounge-irc/0 remove-user name=myuser
```

## Authors
* Marco Ceppi <marco@ceppi.net>
* James Beedy <jamesbeedy@gmail.com>

### License

The MIT License (MIT) (see copyright file in this directory)

Copyright (c) 2017 James Beedy <jamesbeedy@gmail.com>
