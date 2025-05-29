import argparse
import subprocess
import shlex


def run_commands(commands):
    for cmd in commands:
        print(cmd)
        subprocess.run(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser(
        description="Run crackmapexec enumeration commands sequentially.",
        add_help=False
    )
    parser.add_argument('-u', '--user', required=True, help='Username')
    parser.add_argument('-p', '--password', help='Password')
    parser.add_argument('-h', '--hash', dest='hash', help='NTLM hash')
    parser.add_argument('-d', '--domain', required=True, help='Domain name')
    parser.add_argument('-ip', '--ip', dest='ip', required=True, help='Target IP address')
    parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')

    args = parser.parse_args()

    if not args.password and not args.hash:
        parser.error('You must provide either --password or --hash.')

    user = args.user
    password = args.password
    hashval = args.hash
    domain = args.domain
    ip = args.ip

    commands = []

    if password:
        pw = shlex.quote(password)
        commands = [
            f"crackmapexec smb {ip} -u {user} -p {pw}",
            f"crackmapexec smb {ip} -u {user} -p {pw} --shares",
            f"crackmapexec ldap {ip} -u {user} -p {pw}",
            f"crackmapexec winrm {ip} -u {user} -p {pw}",
            f"crackmapexec smb {ip} -u {domain}/{user} -p {pw}",
            f"crackmapexec ldap {ip} -u {domain}/{user} -p {pw}",
            f"crackmapexec winrm {ip} -u {domain}{user} -p {pw}",
        ]
    else:
        hv = hashval
        commands = [
            f"crackmapexec smb {ip} -u {user} -H {hv}",
            f"crackmapexec smb {ip} -u {user} -H {hv} --shares",
            f"crackmapexec ldap {ip} -u {user} -H {hv}",
            f"crackmapexec winrm {ip} -u {user} -H {hv}",
            f"crackmapexec smb {ip} -u {domain}/{user} -H {hv}",
            f"crackmapexec ldap {ip} -u {domain}/{user} -H {hv}",
            f"crackmapexec winrm {ip} -u {domain}{user} -H {hv}",
        ]

    run_commands(commands)


if __name__ == '__main__':
    main()
