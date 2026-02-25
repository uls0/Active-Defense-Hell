import socket
import struct
import time
import random
import os

def checksum(source_string):
    sum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def start_icmp_tarpit(whitelist):
    """Escucha peticiones ICMP y responde con retraso artificial"""
    try:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except PermissionError:
        print("[!] Error: ICMP Tarpit requiere privilegios de ROOT.")
        return

    print("[📡] ICMP Tarpit iniciado. Retrasando respuestas de PING...")

    while True:
        # Recibir paquete
        packet, addr = raw_socket.recvfrom(1024)
        ip_header = packet[:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        src_ip = socket.inet_ntoa(iph[8])
        
        if src_ip in whitelist: continue

        # Extraer ICMP Header
        icmp_packet = packet[20:28]
        icmp_type, code, my_checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_packet)

        # 8 = Echo Request (Ping)
        if icmp_type == 8:
            # Latencia artificial: de 2 a 5 segundos
            delay = random.uniform(2.0, 5.0)
            time.sleep(delay)
            
            # Construir respuesta (Type 0 = Echo Reply)
            header = struct.pack("bbHHh", 0, 0, 0, packet_id, sequence)
            data = packet[28:] # Mantener la misma carga que envió el atacante
            my_checksum = checksum(header + data)
            header = struct.pack("bbHHh", 0, 0, socket.htons(my_checksum), packet_id, sequence)
            
            # Enviar respuesta
            raw_socket.sendto(header + data, (src_ip, 1))
            print(f"[🐢] PING de {src_ip} retrasado {round(delay, 2)}s.")
