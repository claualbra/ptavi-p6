#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys

# Cliente UDP simple.
# Dirección IP del servidor.
try:
    METODO = sys.argv[1]
    ADRESS = sys.argv[2].split(':')[0]
    SERVER = ADRESS.split('@')[1]
    PORT = int(sys.argv[2].split(':')[1])
except (IndexError, ValueError):
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print("Enviando:", METODO + ' sip:' + ADRESS + ' SIP/2.0')
    my_socket.send(bytes(METODO + ' sip:' + ADRESS + ' SIP/2.0', 'utf-8')
                   + b'\r\n\r\n')
    try:
        data = my_socket.recv(1024)
    except ConnectionRefusedError:
        sys.exit("Error en la conexion")
    recb = data.decode('utf-8').split()
    print('Recibido -- ', data.decode('utf-8'))
    if METODO == 'INVITE':
        if recb[2] == 'Trying' and recb[5] == "Ringing" and recb[8] == "OK":
            my_socket.send(bytes('ACK sip:' + ADRESS + ' SIP/2.0', 'utf-8')
                           + b'\r\n\r\n')
    if METODO == 'BYE':
        if data.decode('utf-8') == "SIP/2.0 200 OK\r\n\r\n":
            print("Terminando socket...")
print("Fin.")
