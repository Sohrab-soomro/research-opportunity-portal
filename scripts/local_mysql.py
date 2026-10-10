"""Windows project-local MySQL lifecycle. No system service or global settings changed.

Usage: .venv/Scripts/python.exe scripts/local_mysql.py setup|start|stop|status
Install Oracle MySQL 8.4 before setup. Local secrets/data are excluded from Git.
"""
from pathlib import Path
import argparse
import json
import os
import secrets
import subprocess
import sys
import time
import mysql.connector

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / '.local'
ENV = ROOT / 'backend/.env'
PORT = 3307


def credentials():
    return json.loads((LOCAL / 'admin.json').read_text())


def connect():
    return mysql.connector.connect(host='127.0.0.1', port=PORT, user='root',
                                   password=credentials()['password'], connection_timeout=2)


def ready():
    try:
        conn = connect()
        conn.close()
        return True
    except (mysql.connector.Error, FileNotFoundError):
        return False


def start(bootstrap=False):
    if ready():
        print('Project MySQL is already running on 127.0.0.1:3307.')
        return
    config = LOCAL / 'mysql.ini'
    if not config.exists():
        raise RuntimeError('Run setup first.')
    command = [credentials()['executable'], f'--defaults-file={config}']
    if bootstrap:
        command.append(f'--init-file={(LOCAL / "bootstrap.sql").as_posix()}')
    with (LOCAL / 'startup.log').open('ab') as log:
        process = subprocess.Popen(command, stdout=log, stderr=log,
                                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    for _ in range(60):
        if ready():
            print('Project MySQL started on 127.0.0.1:3307.')
            return
        if process.poll() is not None:
            break
        time.sleep(0.5)
    raise RuntimeError('MySQL did not become ready; inspect private .local logs locally.')


def setup():
    if LOCAL.exists() or ENV.exists():
        raise RuntimeError('Existing .local or backend/.env detected. Setup refuses to overwrite it; use start/status.')
    binary = Path(os.environ.get('MYSQLD_PATH', r'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe'))
    if not binary.exists():
        raise RuntimeError('Install Oracle MySQL 8.4, or set MYSQLD_PATH to mysqld.exe.')
    # Check the chosen port before creating anything. Never displace another server.
    import socket
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', PORT))
    LOCAL.mkdir()
    if os.name == 'nt':
        identity = subprocess.check_output(['whoami'], text=True).strip()
        subprocess.run(['icacls', str(LOCAL), '/inheritance:r', '/grant:r',
                        f'{identity}:(OI)(CI)F', 'SYSTEM:(OI)(CI)F'], check=True, stdout=subprocess.DEVNULL)
    root_password = secrets.token_urlsafe(36)
    app_password = secrets.token_urlsafe(36)
    (LOCAL / 'admin.json').write_text(json.dumps({'password': root_password, 'executable': str(binary)}))
    data = LOCAL / 'mysql-data'
    config = ('[mysqld]\n'
              f'basedir="{binary.parent.parent.as_posix()}"\n'
              f'datadir="{data.as_posix()}"\n'
              f'port={PORT}\nbind-address=127.0.0.1\nmysqlx=0\n'
              f'log-error="{(LOCAL / "mysql-error.log").as_posix()}"\n'
              'character-set-server=utf8mb4\n')
    (LOCAL / 'mysql.ini').write_text(config)
    with (LOCAL / 'initialize.log').open('wb') as log:
        subprocess.run([str(binary), f'--defaults-file={LOCAL / "mysql.ini"}', '--initialize-insecure'],
                       check=True, stdout=log, stderr=log,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    # The init file runs before the listener accepts connections. No password goes in argv.
    bootstrap = LOCAL / 'bootstrap.sql'
    bootstrap.write_text(
        f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{root_password}';\n"
        f"CREATE USER 'portal_app'@'localhost' IDENTIFIED BY '{app_password}';\n"
        "GRANT SELECT, INSERT, UPDATE, DELETE ON research_portal.* TO 'portal_app'@'localhost';\n"
        "GRANT CREATE, DROP, SELECT, INSERT, UPDATE, DELETE ON `research\\_portal\\_test\\_%`.* TO 'portal_app'@'localhost';\n")
    start(bootstrap=True)
    with connect() as conn:
        with conn.cursor() as cursor:
            for filename in ['schema.sql', 'seed.sql']:
                sql = (ROOT / 'database' / filename).read_text()
                for statement in sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
            conn.commit()
    ENV.write_text(f'DB_HOST=127.0.0.1\nDB_PORT={PORT}\nDB_USER=portal_app\nDB_PASSWORD={app_password}\nDB_NAME=research_portal\nFLASK_PORT=5000\n')
    if os.name == 'nt':
        subprocess.run(['icacls', str(ENV), '/inheritance:r', '/grant:r',
                        f'{identity}:F', 'SYSTEM:F'], check=True, stdout=subprocess.DEVNULL)
    bootstrap.unlink()
    print('Created research_portal, two demo records, restricted app account and private backend/.env.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['setup', 'start', 'stop', 'status'])
    action = parser.parse_args().action
    if action == 'setup':
        setup()
    elif action == 'start':
        start()
    elif action == 'stop':
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SHUTDOWN')
        print('Project MySQL shutdown requested; stored data is preserved.')
    else:
        with connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT VERSION()')
                print('MySQL version:', cursor.fetchone()[0])
                cursor.execute('SELECT COUNT(*) FROM research_portal.opportunities')
                print('Stored opportunities:', cursor.fetchone()[0])


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Never expose connector details or passwords on failure.
        print('Local MySQL action failed:', type(error).__name__)
        if isinstance(error, RuntimeError):
            print(str(error))
        sys.exit(1)
