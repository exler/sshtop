from abc import ABC, abstractmethod
from typing import Any

from sshtop.result import SSHResult


class Command(ABC):
    COMMAND_STR: str

    def __call__(self) -> str:
        return self.COMMAND_STR

    @staticmethod
    @abstractmethod
    def parse(result: SSHResult) -> Any:
        pass


class UptimeCommand(Command):
    COMMAND_STR = "cut -d. -f1 /proc/uptime"

    @staticmethod
    def parse(result: SSHResult) -> Any:
        up = int(result.stdout)
        seconds = up % 60
        minutes = int((up / 60) % 60)
        hours = int((up / 3600) % 24)
        days = int(up / 86400)
        return seconds, minutes, hours, days


class LoadAvgCommand(Command):
    COMMAND_STR = "cat /proc/loadavg"

    @staticmethod
    def parse(result: SSHResult) -> Any:
        loadavg = result.stdout.rstrip("\n\r").split()[:3]
        return loadavg


class MemoryCommand(Command):
    COMMAND_STR = "cat /proc/meminfo"

    @staticmethod
    def parse(result: SSHResult) -> Any:
        memory = result.stdout.split("\n")
        memfree = int(memory[1].split()[1]) / 1024
        memtotal = int(memory[0].split()[1]) / 1024
        return memfree, memtotal


class IPCommand(Command):
    COMMAND_STR = "hostname -I"

    @staticmethod
    def parse(result: SSHResult) -> Any:
        ips = result.stdout.split()
        return ips
