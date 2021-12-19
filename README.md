# sshtop

`sshtop` connects to remote systems over SSH and gathers common information about the system.

Only Linux systems can be monitored at this moment.

## Installation

Install using pip:
```bash
$ pip install sshtop
```

## Usage

```bash
$ sshtop [-h] [-p PORT] [-i IDENTITY_FILE] destination
```

If a keyfile has not been supplied, `sshtop` will automatically search for a valid key through a SSH agent.

## License

Copyright (c) 2019-2021 by ***Kamil Marut***.

`sshtop` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
