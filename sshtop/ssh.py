import logging
from typing import Optional

from paramiko import MissingHostKeyPolicy, SSHClient
from paramiko.ssh_exception import SSHException

from sshtop.commands import Command
from sshtop.result import SSHResult

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class PromptUserPolicy(MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):  # noqa
        add_host = input(f"Unknown {key.get_name()} host key for {hostname}. Add? [y/N] ")
        if add_host.lower() == "y":
            client._host_keys.add(hostname, key.get_name(), key)
            if client._host_keys_filename is not None:
                client.save_host_keys(client._host_keys_filename)
        else:
            raise SSHException(f"Server {hostname} not found in known_hosts.")


class SSH:
    client: SSHClient

    is_connected: bool

    def __init__(self) -> None:
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(PromptUserPolicy)

        self.is_connected = False

    def connect(
        self,
        hostname: str,
        port: int = 22,
        username: Optional[str] = None,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        self.client.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            key_filename=private_key,
            timeout=timeout,
        )

        self.is_connected = True

    def close(self) -> None:
        self.client.close()

    def exec(self, command: Command, timeout: int = 5) -> Optional[SSHResult]:
        if not self.is_connected:
            logging.info("Please run the `connect` method before executing commands")
            return None

        try:
            _, stdout, stderr = self.client.exec_command(command(), timeout=timeout)  # nosec
            return SSHResult(stdout, stderr)
        except SSHException:
            return None
