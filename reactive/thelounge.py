import os
import subprocess

from charms.reactive import (
    endpoint_from_flag,
    hook,
    remove_state,
    set_flag,
    when,
    when_not,
)

from charmhelpers.core import host

from charmhelpers.core.hookenv import (
    application_version_set,
    config,
    status_set,
    open_port,
    close_port,
)

from charmhelpers.core.templating import render


LOUNGE_HOME = os.path.join(
    '/', 'var', 'snap', 'theloungeirc', 'common', 'etc', 'thelounge')


@when('snap.installed.theloungeirc')
@when_not('thelounge.available')
def configure_thelounge():
    status_set('maintenance', 'Configuring thelounge irc')

    render(
        source='config.js.j2',
        target=os.path.join(LOUNGE_HOME, 'config.js'),
        context={
            'public': 'true' if config('public') else 'false',
            'proxy': 'true' if config('reverseproxy') else 'false',
            'port': config('port')
        },
    )

    render(
        source='_.json',
        target=os.path.join(LOUNGE_HOME, 'users', '_.json'),
        context={}
    )

    if host.service_running('snap.theloungeirc.thelounge'):
        host.service_restart('snap.theloungeirc.thelounge')
    else:
        host.service_start('snap.theloungeirc.thelounge')

    application_version_set(lounge_version())
    update()

    set_flag('thelounge.available')
    status_set('active', 'thelounge configured')


@when('endpoint.http.joined')
@when('thelounge.available')
def configure_website():
    endpoint = endpoint_from_flag('endpoint.http.joined')
    endpoint.configure(port=config('port'))


@when('thelounge.available')
def open_lounge_port():
    open_port(config('port'))


@when_not('thelounge.available')
def close_lounge_port():
    close_port(config('port'))


@hook('update-status')
def update():
    extra = 'running' if host.service_running('snap.theloungeirc.thelounge') else 'stopped'
    status_set('active', 'version %s - %s' % (lounge_version(), extra))


@hook('upgrade-charm')
def set_revision_as_version():
    application_version_set(lounge_version())


def lounge_version():
    return subprocess.check_output(
        ['theloungeirc.thelounge-cli', '--version']).decode('UTF-8').strip()
