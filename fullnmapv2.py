import argparse
import subprocess
import re


def run_command(cmd):
    """Run a shell command and print output line by line."""
    print(cmd)
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output_lines = []
    for line in process.stdout:
        print(line, end="")
        output_lines.append(line)
    process.wait()
    return "".join(output_lines)


def parse_ports_and_services(nmap_output):
    """Return list of (port, service) from nmap output."""
    results = []
    for line in nmap_output.splitlines():
        match = re.match(r"^(\d+)/tcp\s+open\s+(\S+)", line.strip())
        if match:
            results.append((match.group(1), match.group(2)))
    return results


def print_summary(ports_and_services):
    if not ports_and_services:
        print("\nNo open ports discovered.\n")
        return

    port_width = max(len(p) for p, _ in ports_and_services)
    service_width = max(len(s) for _, s in ports_and_services)
    line_fmt = f"{{:<{port_width}}} | {{:<{service_width}}}"

    print("\nDiscovered Ports and Services:")
    print(line_fmt.format("Port", "Service"))
    print("-" * (port_width + service_width + 3))
    for port, service in ports_and_services:
        print(line_fmt.format(port, service))
    print()


def main():
    parser = argparse.ArgumentParser(description="Run sequential nmap scans")
    parser.add_argument("-ip", required=True, help="Target host or IP")
    parser.add_argument(
        "-Pn", action="store_true", dest="pn", help="Add -Pn to nmap commands"
    )
    args = parser.parse_args()

    ip = args.ip
    pn_flag = "-Pn" if args.pn else ""

    # Command 1: Fast full TCP scan
    cmd1 = f"sudo nmap {pn_flag} -p- --min-rate 10000 -oA enum/fast-alltcp {ip}".strip()
    output = run_command(cmd1)

    # Parse ports and services from the first scan
    ports_services = parse_ports_and_services(output)
    ports = ",".join(port for port, _ in ports_services)

    commands = []

    if ports:
        commands.append(
            f"sudo nmap {pn_flag} -sCV -p {ports} -oA enum/sCV-specific {ip}"
        )
        commands.append(
            f"sudo nmap {pn_flag} --script vuln -p {ports} -oA enum/vulns-specific {ip}"
        )
    else:
        commands.append("echo 'No open ports found for sCV scan'")
        commands.append("echo 'No open ports found for vuln scan'")

    commands.append(f"sudo nmap {pn_flag} -v -oA enum/slow-tcp {ip}")
    commands.append(
        f"sudo nmap {pn_flag} -sU --min-rate 10000 -p- -oA enum/alludp {ip}"
    )
    commands.append(f"sudo nmap {pn_flag} -p- -v -oA enum/slow-alltcp {ip}")

    for cmd in commands:
        run_command(cmd)

    print_summary(ports_services)


if __name__ == "__main__":
    main()
