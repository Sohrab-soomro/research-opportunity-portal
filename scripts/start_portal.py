"""Start this project's MySQL and Flask server, then open the frontend."""
from pathlib import Path
import subprocess
import sys
import urllib.request
import urllib.error
import time
import webbrowser

ROOT = Path(__file__).resolve().parent.parent


def healthy():
    try:
        with urllib.request.urlopen('http://localhost:5000/api/opportunities', timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, OSError):
        return False


def main():
    subprocess.run([sys.executable, str(ROOT / 'scripts/local_mysql.py'), 'start'], check=True)
    if healthy():
        print('Portal is already running at http://localhost:5000')
        webbrowser.open('http://localhost:5000')
        return
    server = subprocess.Popen([sys.executable, str(ROOT / 'backend/app.py')], cwd=ROOT)
    try:
        for _ in range(40):
            if healthy():
                webbrowser.open('http://localhost:5000')
                print('Portal ready. Keep this terminal open; Ctrl+C stops Flask.')
                server.wait()
                return
            if server.poll() is not None:
                raise RuntimeError('Flask exited; check the messages above.')
            time.sleep(0.25)
        raise RuntimeError('Flask did not become ready; inspect the terminal.')
    except KeyboardInterrupt:
        pass
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=10)


if __name__ == '__main__':
    main()
