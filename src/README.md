# TheLounge IRC
This charm provides TheLounge IRC, the self-hosted web IRC client.

# Simple Deploy
1. Deploy the charm!
`juju deploy thelounge`

2. Add a user 
`juju run-action thelounge/0 add-user username="myuser" password="mypassword"`

3. Login to the webui with the user creds created in #2


# Deploy with reverse proxy
```bash
juju deploy haproxy
juju deploy thelounge
juju relate thelounge haproxy
```

# User Lifecycle
This charm ships with a few user management lifecycle actions:
```bash
# Add User
juju run-action thelounge/0 add-user username="myuser" password="mypassword"

# Delete User
juju run-action thelounge/0 del-user username="myuser"

# Reset Password
juju run-action thelounge/0 reset-password username="myuser" password="mynewpassword"
```

## Authors
* James Beedy <jamesbeedy@gmail.com>

## Copyright
* AGPLv3 (see `copyright` file for full text)
