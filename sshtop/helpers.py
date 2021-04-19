# -*- coding: utf-8 -*-

from os import name, system


class Colors:
    BLUE = "\33[94m"
    RED = "\33[91m"
    YELLOW = "\33[93m"
    GREEN = "\33[1;32m"
    WHITE = "\33[97m"
    END = "\33[0m"


def print_header(string):
    print(Colors.YELLOW + string + Colors.END)


def print_body(string):
    print(Colors.WHITE + string + Colors.END)


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")
