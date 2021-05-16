#!/usr/bin/env python
# encoding: utf-8

import subprocess
import optparse
import re

# Função que lê os argumentos inseridos pelo usuário
def pegar_argumentos():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Argumento que define qual interface terá seu MAC address trocado")
    parser.add_option("-m", "--mac", dest="novo_mac",
                      help="Argumento que define o novo MAC address")
    (opcoes, argumentos) = parser.parse_args()
    if not opcoes.interface:
        parser.error("[-] Especifique a interface")
    elif not opcoes.novo_mac:
        parser.error("[-] Especifique o novo MAC address da interface")
    return opcoes

# Função que troca o MAC address da interface pelo inserido pelo usuário
def mudar_mac(interface, novo_mac):
    print("[+] Trocando o MAC address de " + interface + " para " + novo_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", novo_mac])
    subprocess.call(["ifconfig", interface, "up"])

# Função que pega o valor do MAC address atual da interface
def pegar_mac_atual(interface):
    resultado_ifconfig = subprocess.check_output(["ifconfig", interface])
    resultado_busca_mac_atual = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(resultado_ifconfig))
    if resultado_busca_mac_atual:
        return resultado_busca_mac_atual.group(0)
    else:
        print("[-] Não foi possível encontrar o MAC address da interface")
        exit(0)

# A variável "opcoes" possui os valores da interface e do MAC address queo usuário inseriu.
opcoes = pegar_argumentos()

# A variável "mac_atual" usa a função "pegar_mac_atual" que,
# por sua vez, usa a interface armazenada na variável "opcoes".
mac_atual = pegar_mac_atual(opcoes.interface)
print("[+] MAC address atual: " + str(mac_atual))

# A mesma lógica é aplicada na função "mudar_mac" que recebe os valores inseridos pelo usuário e roda o código.
mudar_mac(opcoes.interface, opcoes.novo_mac)

# A variável "mac_atual" então recebe o valor do MAC address novo e printa como forma de validação.
mac_atual = pegar_mac_atual(opcoes.interface)
if mac_atual == opcoes.novo_mac:
    print("[+] O MAC address foi trocado com sucesso! Seu novo MAC address é: " + mac_atual)
else:
    print("[-] Não foi possível trocar o MAC address")
