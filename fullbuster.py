import argparse

WORDLIST = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"


def commands_for_port(host, port):
    cmds = []
    if port == 80:
        cmds.append(
            f"gobuster dir -u http://{host}/ -w {WORDLIST} -t 200 -o gobuster/gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u http://{host}/api/ -w {WORDLIST} -t 200 -o gobuster/gobusterInicial"
        )
    elif port == 443:
        cmds.append(
            f"gobuster dir -u https://{host}/ -k -w {WORDLIST} -t 200 -o gobuster/443gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u https://{host}/ -w {WORDLIST} -t 200 -o gobuster/443gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u https://{host}/api/ -w {WORDLIST} -t 200 -o gobuster/443gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u https://{host}/ -k -w {WORDLIST} -t 200 -o gobuster/20000gobusterInicial --exclude-length 4867"
        )
        cmds.append(
            f"gobuster dir -u https://{host}/api/ -k -w {WORDLIST} -t 200 -o gobuster/20000gobusterInicial --exclude-length 4867"
        )
    else:
        cmds.append(
            f"gobuster dir -u http://{host}:{port}/ -w {WORDLIST} -t 200 -o gobuster/{port}gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u http://{host}/api -w {WORDLIST} -t 200 -o gobuster/gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u https://{host}:{port}/ -w {WORDLIST} -t 200 -o gobuster/{port}gobusterInicial"
        )
        cmds.append(
            f"gobuster dir -u https://{host}/api -w {WORDLIST} -t 200 -o gobuster/gobusterInicial"
        )
    return cmds


def main():
    parser = argparse.ArgumentParser(
        description="Generate gobuster commands", add_help=False
    )
    parser.add_argument('-u', dest='host', required=True, help='Hostname or IP')
    parser.add_argument('-p', dest='ports', nargs='*', default=[], help='Additional ports')
    parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')
    args = parser.parse_args()

    host = args.host
    ports = set(int(p) for p in args.ports)
    ports.update([80, 443])
    for port in sorted(ports):
        print(f"{port}:")
        for cmd in commands_for_port(host, port):
            print(cmd)
        print()

    print("#cuando se obtiene error: => 200 (Length: 4867).")
    print(
        f"gobuster dir -u https://{host}/ -k -w {WORDLIST} -t 200 -o gobuster/20000gobusterInicial --exclude-length 4867"
    )
    print()
    print("#por .php,aspx,asp,txt")
    print(
        f"gobuster dir -u http://{host}/ -w {WORDLIST} -x php,txt -t 200 -o gobuster/gobusterFileType"
    )


if __name__ == '__main__':
    main()
