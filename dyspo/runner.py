import subprocess
import os
import sys
import asyncio
from threading import Thread, Event
from aiohttp import web

from dyspo.reloader import DirectoryMonitor


class ServerRunner(object):
    def __init__(self, api, event=None):
        self.api = api
        self.event = event or Event()
        self.loop = asyncio.new_event_loop()

    def run_server(self, debug=False, **kwargs):
        try:
            if debug:
                self.run_with_reloader(**kwargs)

            self._run_api(**kwargs)

        except KeyboardInterrupt:
            pass

    def listen_for_changes(self):
        try:
            while True:
                self.event.wait(timeout=1.0)

                if self.event.is_set():
                    print('Changes detected. Restarting server...\n')
                    self._trigger_reload()

        except KeyboardInterrupt:
            print('\nUser requested quit, exiting.')

    def run_threads(self, **kwargs):
        runner = Thread(target=self._run_api, kwargs=kwargs)
        runner.daemon = True
        runner.start()

        monitor = DirectoryMonitor(self.event, daemon=True)
        monitor.start()

    def run_with_reloader(self, **kwargs):
        if os.environ.get('RUN_MAIN') == 'true':
            self.run_threads(**kwargs)
            self.listen_for_changes()
        else:
            sys.exit(self.restart())

    def restart(self):
        # to stop the aiohttp server
        self.loop.call_soon_threadsafe(self._stop_loop)

        while True:
            args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions] + sys.argv
            new_environ = os.environ.copy()
            new_environ['RUN_MAIN'] = 'true'
            exit_code = subprocess.call(args, env=new_environ)
            if exit_code != 3:
                return exit_code

    def _stop_loop(self):
        try:
            self.loop.stop()
            self.loop.close()
        except RuntimeError:
            pass

    def _trigger_reload(self):
        sys.exit(3)

    def _run_api(self, **kwargs):
        try:
            asyncio.set_event_loop(self.loop)
            web.run_app(self.api, handle_signals=False, **kwargs)
        except SystemExit as e:
            print('got system exit: ', e)
