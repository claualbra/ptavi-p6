#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
# Dirección IP del servidor.
try:
    METODO = sys.argv[1]
    ADRESS = sys.argv[2].split(':')[0]
    LOGIN = ADRESS.split('@')[0]
    SERVER = ADRESS.split('@')[1]
    PORT = int(sys.argv[2].split(':')[1])
except (IndexError, ValueError):
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print("Enviando:", METODO + ' sip:' + ADRESS + ' SIP/2.0')
    my_socket.send(bytes(METODO + ' sip:' + ADRESS + ' SIP/2.0', 'utf-8')
                    + b'\r\n\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
