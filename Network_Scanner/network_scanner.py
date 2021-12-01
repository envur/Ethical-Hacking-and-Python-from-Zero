import scapy.all as scapy
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Specify the IP range which you want to scan")
    opts = parser.parse_args()
    if not opts.target:
        parser.error("Specify the IP range! Use -h for help")
    return opts

def scan(ip):
    target_ips = scapy.ARP(pdst=ip)
    broadcast_MAC = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast_ips = broadcast_MAC/target_ips
    answered_list = scapy.srp(arp_broadcast_ips, timeout=2, verbose=False)[0]
    answers_data_list = []
    for answer in answered_list:
        answers_data_list.append({"ip": answer[1].psrc, "mac": answer[1].hwsrc})
    
    return answers_data_list

def print_results(results):
    print("IP Address\t\t\tMAC Address")
    print("--------------------------------------------------")
    
    for item in results:
        print(f'{item["ip"]}\t\t\t{item["mac"]}') 

options = get_args()
results = scan(str(options.target))
print_results(results)
