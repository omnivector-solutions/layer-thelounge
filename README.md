# Lounge IRC
This charm provides Lounge IRC, the self-hosted web IRC client.

# Simple Deploy
```bash
juju deploy lounge-irc
```

# Deploy with reverse proxy
```bash
juju deploy haproxy
juju deploy lounge-irc
juju relate lounge-irc haproxy
```

### License

The MIT License (MIT) (see copyright file in this directory)

Copyright (c) 2017 James Beedy <jamesbeedy@gmail.com>
