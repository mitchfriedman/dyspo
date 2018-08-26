import time
import sys
import os
from threading import Thread, Event


def get_watchable_files():
    for m in list(sys.modules.values()):
        if not hasattr(m, '__file__'):
            continue

        filename = os.path.abspath(getattr(m, '__file__'))

        if filename[-4:] in ('.pyc', '.pyo'):
            filename = filename[:-1]

        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"

        if not os.path.exists(filename):
            continue

        yield filename

    yield os.path.abspath(sys.argv[0])


class Monitor(Thread):
    def __init__(self, event: Event, interval=None, **kwargs):
        super().__init__(**kwargs)
        self.event = event
        self.interval = interval or 0.5

    def run(self):
        while True:
            if self.changes_detected():
                self.event.set()
            time.sleep(self.interval)

    def changes_detected(self):
        return


class DirectoryMonitor(Monitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.watching = {}

    def changes_detected(self) -> bool:
        diffs = False

        for file in get_watchable_files():
            try:
                changed_time = os.path.getmtime(file)
            except FileNotFoundError:
                del self.watching[file]
                continue

            if file not in self.watching:
                self.watching[file] = changed_time
                continue

            if self.watching.get(file) != changed_time:
                self.watching[file] = changed_time
                diffs = True

        return diffs
