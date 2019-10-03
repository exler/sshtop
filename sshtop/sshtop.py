#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse



try:
    from paramiko import SSHClient, ssh_exception

    from monitor import start_monitoring
except ImportError:
    print("[!] Failed to import necessary packages. Please install them first.")
    raise SystemExit(1)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remote server monitoring over SSH.")
    parser.add_argument('-i', '--interval', default=5, type=int,
                        help="Refresh interval in seconds.")
    parser.add_argument('-k', '--private-key-file',
                        help="PEM-formatted private key file to authenticate with.")
    parser.add_argument('host',
                        help="SSH server to connect to, with optional username. Formatted as: user@host")
    parser.add_argument('-p', '--password',
                        help="SSH user password.")
    parser.add_argument('--port', default=22, type=int,
                        help="Port on which the SSH should try connectings. Defaults to 22.")
    args = parser.parse_args()

    if '@' in args.host:
        username, hostname = args.host.split('@')
    else:
        username = None
        hostname = args.host

    client = SSHClient()
    client.load_system_host_keys()

    try:
        client.connect(hostname, port=args.port,
                    username=username, password=args.password,
                    key_filename=args.private_key_file,
                    timeout=10)
    except ssh_exception.AuthenticationException:
        print("[!] Error while trying to authenticate! Please check the password or keyfile.")
        raise SystemExit(1)
    except ssh_exception.SSHException as e:
        print(f"[!] Error while trying to estabilish a SSH session. Error: {e}")
        raise SystemExit(1)

    try:
        start_monitoring(client, args.interval)
    except KeyboardInterrupt:
        raise SystemExit(0)
