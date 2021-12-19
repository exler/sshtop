import os

from paramiko.channel import ChannelFile


def read_channel_file(f: ChannelFile) -> str:
    return f.read().decode("utf-8")


def clear_terminal() -> None:
    if os.name == "nt":
        os.system("cls")  # nosec
    else:
        os.system("clear")  # nosec
