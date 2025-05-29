import argparse
import subprocess
import re


def run_command(cmd):
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output_lines = []
    for line in process.stdout:
        print(line, end='')
        output_lines.append(line)
    process.wait()
    return ''.join(output_lines)


def parse_ports(nmap_output):
    ports = []
    for line in nmap_output.splitlines():
        match = re.match(r"^(\d+)/tcp\s+open", line.strip())
        if match:
            ports.append(match.group(1))
    return ','.join(ports)


def main():
    parser = argparse.ArgumentParser(description="Run sequential nmap scans", add_help=False)
    parser.add_argument('-ip', dest='ip', required=True, help='Target host or IP')
    parser.add_argument('-Pn', dest='pn', action='store_true', help='Add -Pn to nmap commands')
    parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')
    args = parser.parse_args()

    ip = args.ip
    pn_flag = '-Pn' if args.pn else ''

    commands = [
        f"sudo nmap {pn_flag} -p- --min-rate 10000 -oA enum/fast-alltcp {ip}",
        # Commands 2 and 3 will be formatted after parsing ports
        None,
        None,
        f"sudo nmap {pn_flag} -v enum/slow-tcp {ip}",
        f"sudo nmap {pn_flag} -sU --min-rate 10000 -p- -oA enum/alludp {ip}",
        f"sudo nmap {pn_flag} -p- -v -oA enum/slow-alltcp {ip}"
    ]

    output = run_command(commands[0])
    ports = parse_ports(output)

    if ports:
        commands[1] = f"sudo nmap {pn_flag} -sCV -p {ports} -oA enum/sCV-specific {ip}"
        commands[2] = f"sudo nmap {pn_flag} --script vuln -p {ports} -oA enum/vulns-specific {ip}"
    else:
        commands[1] = f"echo 'No open ports found for sCV scan'"
        commands[2] = f"echo 'No open ports found for vuln scan'"

    for cmd in commands[1:]:
        run_command(cmd)


if __name__ == '__main__':
    main()
