from time import sleep

from colorama import Fore, Style

from sshtop.commands import IPCommand, LoadAvgCommand, MemoryCommand, UptimeCommand
from sshtop.ssh import SSH
from sshtop.utils import clear_terminal


class RemoteMonitor:
    def __init__(self, ssh_client: SSH) -> None:
        self.client = ssh_client

        self.c_uptime = UptimeCommand()
        self.c_loadavg = LoadAvgCommand()
        self.c_memory = MemoryCommand()
        self.c_ip = IPCommand()

    def start(self) -> None:
        try:

            ips = self.c_ip.parse(self.client.exec(self.c_ip))

            while True:
                uptime = self.c_uptime.parse(self.client.exec(self.c_uptime))
                loadavg = self.c_loadavg.parse(self.client.exec(self.c_loadavg))
                free_memory, total_memory = self.c_memory.parse(self.client.exec(self.c_memory))

                clear_terminal()
                print(Fore.YELLOW + f"Uptime: {uptime[3]} days, {uptime[2]}h{uptime[1]}m{uptime[0]}s")
                print(Fore.YELLOW + f"Load averages: {loadavg[0]}, {loadavg[1]}, {loadavg[2]}  (1, 5, 15 min)")
                print(Fore.YELLOW + f"Memory: {free_memory:.2f}MB (Free) / {total_memory:.2f}MB (Total)")
                print(Fore.YELLOW + "IP Addresses:\n\t" + Fore.LIGHTYELLOW_EX + "\n\t".join([ip for ip in ips]))

                print(Style.RESET_ALL)
                sleep(5)

        except KeyboardInterrupt:
            return
