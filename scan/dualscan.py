import socket
import subprocess
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor

def scan_ports(ip, max_ports):
    open_ports = []
    for port in range(1, max_ports + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service_info = socket.getservbyport(port)
                except:
                    service_info = "Unknown"
                open_ports.append((port, service_info))
    return open_ports

def get_mac_vendor(mac_address):
    try:
        output = subprocess.check_output(['arp', '-n', mac_address])
        output = output.decode().split('\n')[1]
        vendor = output.split()[2]
        return vendor
    except:
        return "Unknown"

def scan_active_ips(network):
    active_devices = {}
    ip_range = '.'.join(network.split('.')[:-1])
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(subprocess.run, ['ping', '-c', '1', f'{ip_range}.{i}']) for i in range(1, 255)]
        results = [future.result() for future in futures]
    for i, result in enumerate(results, 1):
        if result.returncode == 0:
            mac_address = subprocess.getoutput(f'arp -n {ip_range}.{i} | grep -o -E "([0-9A-Fa-f]{{2}}[:-]){5}([0-9A-Fa-f]{{2}})"')
            mac_address = mac_address.strip()
            vendor = get_mac_vendor(mac_address)
            active_devices[f'{ip_range}.{i}'] = vendor
    return active_devices

def scan_ports_wrapper(ip, max_ports):
    open_ports = scan_ports(ip, max_ports)
    print("Open ports:")
    for port, service_info in open_ports:
        print(f"Opened --> {port} {service_info}")

def scan_active_ips_wrapper(network):
    active_devices = scan_active_ips(network)
    print("Active Devices:")
    for ip, vendor in active_devices.items():
        print(f"IP: {ip}, Device: {vendor}")

def main():
    # Configurando a análise de argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Scan ports or active IPs.')
    parser.add_argument('mode', metavar='MODE', choices=['ports', 'ips'], help='Scan mode (ports or ips)')
    parser.add_argument('-ip', dest='target', metavar='TARGET', type=str, help='Target IP address or network')
    parser.add_argument('-p', dest='max_ports', metavar='MAX_PORTS', type=int, default=1000, help='The maximum number of ports to scan (default: 1000)')
    args = parser.parse_args()

    if args.mode == 'ports':
        if not args.target:
            print("Error: Target IP address not provided.")
            return
        scan_ports_thread = threading.Thread(target=scan_ports_wrapper, args=(socket.gethostbyname(args.target), args.max_ports))
        scan_ports_thread.start()
        scan_ports_thread.join()
    elif args.mode == 'ips':
        if not args.target:
            print("Error: Target network not provided.")
            return
        scan_active_ips_thread = threading.Thread(target=scan_active_ips_wrapper, args=(args.target,))
        scan_active_ips_thread.start()
        scan_active_ips_thread.join()

if __name__ == "__main__":
    main()

