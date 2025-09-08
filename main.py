import os
import sys
import tempfile
from app.interfaces.index import App

def is_already_running():
    lockfile = os.path.join(tempfile.gettempdir(), 'my_app.lock')

    if os.path.exists(lockfile):
        return True

    # Cria o arquivo de lock
    with open(lockfile, 'w') as f:
        f.write(str(os.getpid()))

    return False

def cleanup_lock():
    lockfile = os.path.join(tempfile.gettempdir(), 'my_app.lock')
    if os.path.exists(lockfile):
        os.remove(lockfile)


if is_already_running():
    sys.exit(0)

try:
    app = App()
    app.mainloop()
finally:
    cleanup_lock()