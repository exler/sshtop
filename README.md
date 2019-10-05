# sshtop

`sshtop` connect over SSH to a remote system and displays system metrics (CPU load averages, memory, disks, network interfaces) by running simple Unix commands.

Only Linux systems can be monitored at this moment.

## Installation

Install using pip:
```bash
$ pip install sshtop
```

## Usage

```bash
$ sshtop host [-k PRIVATE_KEY_FILE] [-p PASSWORD]
```

If a valid PEM-formatted keyfile has not been supplied, `sshtop` will automatically search for a valid key through an SSH agent.

## License

Copyright (c) 2019 by ***Kamil Marut***.

`sshtop` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).