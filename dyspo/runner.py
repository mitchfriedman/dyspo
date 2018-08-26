import subprocess
import os
import sys
import asyncio
from threading import Thread, Event
from aiohttp import web

from dyspo.reloader import DirectoryMonitor

EXIT_CODE = 3


def _trigger_reload():
    sys.exit(EXIT_CODE)


class ServerRunner(object):
    def __init__(self, api, event=None):
        self.api = api
        self.event = event or Event()
        self.loop = asyncio.new_event_loop()

    def run_server(self, debug=False, **kwargs):
        try:
            if debug:
                self.run_reloadable(**kwargs)
            self._run_api(**kwargs)
        except KeyboardInterrupt:
            pass

    def run_reloadable(self, **kwargs):
        if os.environ.get('RUN_MAIN') == 'true':
            Thread(target=self._run_api, daemon=True, kwargs=kwargs).start()
            DirectoryMonitor(self.event, daemon=True).start()
            self._listen_for_changes()
        else:
            # the first time this is run, we need to restart with our
            # environment variable set
            sys.exit(self._restart())

    def _listen_for_changes(self):
        try:
            while True:
                self.event.wait(timeout=1.0)

                if self.event.is_set():
                    print('Changes detected. Restarting server...\n')
                    _trigger_reload()

        except KeyboardInterrupt:
            print('\nUser requested quit, exiting.')

    def _restart(self):
        while True:
            args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions] + sys.argv
            new_environ = os.environ.copy()
            new_environ['RUN_MAIN'] = 'true'
            exit_code = subprocess.call(args, env=new_environ)
            if exit_code != 3:
                return exit_code

    def _run_api(self, **kwargs):
        asyncio.set_event_loop(self.loop)
        web.run_app(self.api, handle_signals=False, **kwargs)
