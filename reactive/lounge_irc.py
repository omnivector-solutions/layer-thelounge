import os
import subprocess

from charms.reactive import when, when_not, set_state, hook, remove_state

from charmhelpers.core import host

from charmhelpers.core.hookenv import config
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import open_port
from charmhelpers.core.hookenv import close_port

from charmhelpers.core.templating import render

from charms.layer.nodejs import npm, node_dist_dir


@when('nodejs.available')
@when_not('lounge-irc.installed')
def install_lounge():
    status_set('maintenance', 'installing lounge-irc')
    npm('-g', 'install', 'thelounge')

    render(
        source='config.js.j2',
        target=os.path.join(node_dist_dir(), 'config.js'),
        context={
            'public': 'true' if config('public') else 'false',
            'port': config('port')
        },
    )

    set_state('lounge-irc.installed')
    remove_state('lounge-irc.started')
    status_set('active', 'lounge-irc installed')


@when('website.available')
@when('lounge-irc.installed')
def configure_website(website):
    website.configure(port=config('port'))


@when('lounge-irc.installed')
@when_not('lounge-irc.started')
def start():
    render(
        source='lounge-irc.service.j2',
        target='/etc/systemd/system/lounge-irc.service',
        context={
            'home': node_dist_dir(),
        },
    )

    if not config('public'):
        users_dir = os.path.join(node_dist_dir(), 'users')
        if not os.path.exists(users_dir):
            os.mkdir(users_dir)

        render(source='_.json', target=os.path.join(users_dir, '_.json'), context={})

    if host.service_running('lounge-irc'):
        host.service_restart('lounge-irc')
    else:
        host.service_start('lounge-irc')

    set_state('lounge-irc.started')
    update()


@when('lounge-irc.started')
def ports():
    open_port(config('port'))


@when_not('lounge-irc.started')
def close():
    close_port(config('port'))


@hook('update-status')
def update():
    extra = 'running' if host.service_running('lounge-irc') else 'stopped'
    status_set('active', 'version %s - %s' % (lounge_version(), extra))


@when_not('nodejs.available')
def reset():
    remove_state('lounge-irc.installed')


def lounge_version():
    return subprocess.check_output(['lounge', '--version']).decode('UTF-8').strip()

