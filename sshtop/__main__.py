import argparse
from getpass import getpass, getuser

from paramiko.ssh_exception import AuthenticationException, SSHException

from sshtop.monitor import RemoteMonitor
from sshtop.ssh import SSH


def main() -> None:
    parser = argparse.ArgumentParser(description="Remote server monitoring over SSH.")
    parser.add_argument("destination", help="SSH server destination, specified as [user@]hostname.")
    parser.add_argument("-p", "--port", default=22, type=int, help="SSH server port (default: 22)")
    parser.add_argument("-i", "--identity-file", help="PEM-formatted private key file to authenticate with.")
    args = parser.parse_args()

    if "@" in args.destination:
        username, hostname = args.destination.split("@")
    else:
        username = getuser().lower()
        hostname = args.destination

    client = SSH()

    try:
        client.connect(hostname, port=args.port, username=username, private_key=args.identity_file)
    except AuthenticationException:
        password = getpass(f"{username}@{hostname}'s password: ")
        client.connect(hostname, port=args.port, username=username, password=password)
    except SSHException as e:
        print(e)
        exit(1)

    monitor = RemoteMonitor(client)
    monitor.start()

    client.close()


if __name__ == "__main__":
    main()
