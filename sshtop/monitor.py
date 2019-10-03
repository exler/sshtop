from time import sleep

import helpers

def get_hostname(ssh_client):
    stdout = ssh_client.exec_command('hostname')[1]

    return stdout.read().decode('utf-8').rstrip('\n\r')

def get_uptime(ssh_client):
    stdout = ssh_client.exec_command('/usr/bin/cut -d. -f1 /proc/uptime')[1]

    up = int(stdout.read().decode('utf-8'))
    secs = up % 60
    mins = int((up / 60) % 60)
    hours = int((up / 3600) % 24)
    days = int(up / 86400)

    return f"{days} days, {hours}h{mins}m{secs}s"


def get_loadavg(ssh_client):
    stdout = ssh_client.exec_command('cat /proc/loadavg')[1]

    loadavg = stdout.read().decode('utf-8').rstrip('\n\r').split()

    return f"{loadavg[0]}, {loadavg[1]}, {loadavg[2]}  (1, 5, 15 min)"

def get_memory(ssh_client):
    stdout = ssh_client.exec_command('cat /proc/meminfo')[1]

    memory = stdout.read().decode('utf-8').split('\n')
    memfree = int(memory[1].split()[1]) / 1024
    memtotal = int(memory[0].split()[1]) / 1024
    swapfree = int(memory[15].split()[1])
    swaptotal = int(memory[14].split()[1])
    buffers = int(memory[3].split()[1]) / 1024
    cached = int(memory[4].split()[1]) / 1024

    return f"""ram: {memfree:.2f}MB (Free) / {memtotal:.2f}MB (Total)
        swap: {swapfree:.2f}kB (Free) / {swaptotal:.2f}kB (Total)
        buffers: {buffers:.2f}MB
        cached: {cached:.2f}MB"""

def get_filesystems(ssh_client):
    stdout = ssh_client.exec_command('df -h')[1]

    filesystems = stdout.read().decode('utf-8').split('\n')[1:-1]

    return filesystems

def get_networks(ssh_client):
    stdout = ssh_client.exec_command('ifconfig eth0')[1]
    eth = stdout.read().decode('utf-8')

    stdout = ssh_client.exec_command('ifconfig wifi0')[1]
    wifi = stdout.read().decode('utf-8')

    if eth and wifi:
        return f"""{helpers.format_network_interface('eth0', eth)}
            {helpers.format_network_interface('wifi0', wifi)}
        """
    elif eth:
        return helpers.format_network_interface('eth0', eth)
    elif wifi:
        return helpers.format_network_interface('wifi0', wifi)
    else:
        return "No Ethernet or WiFi interfaces found!"



def start_monitoring(ssh_client, interval):
    hostname = get_hostname(ssh_client)

    while True:
        uptime = get_uptime(ssh_client)
        loadavg = get_loadavg(ssh_client)
        memory = get_memory(ssh_client)
        filesystems = get_filesystems(ssh_client)
        networks = get_networks(ssh_client)

        helpers.clear_screen()

        print(f"Hostname: {hostname}")
        print(f"Uptime: {uptime}")

        print(f"\nLoad:")
        print(f"\t{loadavg}")

        print(f"\nMemory:")
        print(f"\t{memory}")

        print(f"\nFilesystems:")
        for filesystem in filesystems:
            filesystem = filesystem.split()
            if not len(filesystem[2]) == 1:
                print(f"\t{filesystem[5]}: {filesystem[2]} used out of {filesystem[1]}")

        print(f"\nNetwork Interfaces:")
        print(f"\t{networks}")

        sleep(interval)