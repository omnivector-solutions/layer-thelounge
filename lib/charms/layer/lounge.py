import os
import subprocess


class LoungeCLIError(Exception):
    pass


class Lounge(object):
    def __init__(self, home):
        self.home = home
        self.users_dir = os.path.join(self.home, 'users')

    def add(self, name, password):
        cmd = ' '.join(self._prep(['add', name]))
        try:
            subprocess.check_call('echo %s | %s' % (password, cmd), shell=True)
        except subprocess.CalledProcessError:
            raise LoungeCLIError('%s failed' % cmd)

    def list(self):
        return self._run(['list']).split()[2::2]

    def remove(self, name):
        if not os.path.exists(os.path.join(self.users_dir, '%s.json' % name)):
            return

        try:
            self._run(['remove', name])
        except subprocess.CalledProcessError:
            raise LougeCLIError('removing %s failed' % name)

    def _prep(self, cmd):
        return ['lounge', '--home', self.home] + cmd

    def _run(self, cmd):
        return subprocess.check_output(self._prep(cmd)).decode('UTF-8').strip()
