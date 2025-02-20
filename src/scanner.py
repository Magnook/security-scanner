import os
import socket
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def check_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                print(f"[+] Porta aberta encontrada: {port}")
                return port
    except:
        return None

def check_open_ports(target, port_range):
    open_ports = []
    print(f"[+] Verificando portas abertas em {target}...")

    # Cria um pool de threads
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_port, target, port): port for port in range(*port_range)}
        
        # Usando tqdm para barra de progresso
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning Ports"):
            port = future.result()
            if port:
                open_ports.append(port)

    print("\n[!] Scan finalizado!")
    print(f"Portas abertas: {open_ports}" if open_ports else "Nenhuma porta aberta encontrada.")
    return open_ports



def check_running_processes():
    print("\n[+] Verificando processos em execução...")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes

def check_network_info():
    print("\n[+] Verificando informações de rede...")
    net_info = psutil.net_if_addrs()
    net_stats = psutil.net_if_stats()
    network_data = {}
    for interface, addrs in net_info.items():
        network_data[interface] = {
            'addresses': [addr.address for addr in addrs],
            'status': net_stats[interface].isup
        }
    return network_data

def main():
    print("\n[=== Security Scanner Inicial ===]")
    target = socket.gethostbyname(socket.gethostname())
    print(f"[+] IP do alvo: {target}")

    open_ports = check_open_ports(target, (20, 1025))
    if open_ports:
        print(f"\n[!] Portas abertas encontradas: {open_ports}")
    else:
        print("\n[+] Nenhuma porta aberta encontrada no intervalo especificado.")

    processes = check_running_processes()
    print(f"\n[+] Processos em execução: {len(processes)}")
    for proc in processes[:10]:  # Mostra só os 10 primeiros pra não poluir a saída
        print(f"PID: {proc['pid']}, Nome: {proc['name']}, Usuário: {proc['username']}")

    network_info = check_network_info()
    print("\n[+] Informações de rede:")
    for interface, info in network_info.items():
        print(f"Interface: {interface}")
        print(f"  Endereços: {info['addresses']}")
        print(f"  Status: {'Ativa' if info['status'] else 'Inativa'}")

if __name__ == "__main__":
    main()
