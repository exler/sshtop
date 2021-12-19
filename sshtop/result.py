from dataclasses import dataclass

from paramiko.channel import ChannelFile

from sshtop.utils import read_channel_file


@dataclass
class SSHResult:
    stdout: str
    stderr: str

    def __init__(self, stdout: ChannelFile, stderr: ChannelFile) -> None:
        self.stdout = read_channel_file(stdout)
        self.stderr = read_channel_file(stderr)
