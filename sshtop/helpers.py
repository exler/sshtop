from os import name, system

def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def format_network_interface(interface, ifconfig):
    rows = ifconfig.split('\n')[:-2]
    ipv4 = rows[1].split()[1]
    ipv6 = rows[2].split()[1]
    rx = rows[4].split()[5][1:] + rows[4].split()[6][:-1]
    tx = rows[6].split()[5][1:] + rows[4].split()[6][:-1]

    return f"""{interface} - {ipv4}, {ipv6}
          rx = {rx}, tx = {tx}
    """