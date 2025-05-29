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


def parse_ports_and_services(nmap_output):
    port_services = {}
    for line in nmap_output.splitlines():
        match = re.match(r"^(\d+)/tcp\s+open\s+(\S+)", line.strip())
        if match:
            port = match.group(1)
            service = match.group(2)
            port_services[port] = service
    return port_services


def print_summary(port_services):
    if not port_services:
        print("No open ports discovered.")
        return

    port_width = max(len('Port'), max((len(p) for p in port_services), default=0))
    service_width = max(len('Service'), max((len(s) for s in port_services.values()), default=0))

    sep = "+" + "-" * (port_width + 2) + "+" + "-" * (service_width + 2) + "+"
    header = f"| {'Port'.ljust(port_width)} | {'Service'.ljust(service_width)} |"

    print(sep)
    print(header)
    print(sep)
    for port in sorted(port_services, key=lambda x: int(x)):
        service = port_services[port]
        print(f"| {port.ljust(port_width)} | {service.ljust(service_width)} |")
    print(sep)


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
        f"sudo nmap {pn_flag} -sU --min-rate 10000 -p- -oA enum/alludp {ip}"
    ]

    output = run_command(commands[0])
    port_services = parse_ports_and_services(output)
    ports = ','.join(port_services.keys())

    if ports:
        commands[1] = f"sudo nmap {pn_flag} -sCV -p {ports} -oA enum/sCV-specific {ip}"
        commands[2] = f"sudo nmap {pn_flag} --script vuln -p {ports} -oA enum/vulns-specific {ip}"
    else:
        commands[1] = f"echo 'No open ports found for sCV scan'"
        commands[2] = f"echo 'No open ports found for vuln scan'"

    for cmd in commands[1:]:
        run_command(cmd)

    print_summary(port_services)


if __name__ == '__main__':
    main()
