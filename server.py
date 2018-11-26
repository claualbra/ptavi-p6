#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """Escribe dirección y puerto del cliente (de tupla client_address)."""
        print("La IP y el puerto del cliente es: " + str(self.client_address))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            linea = line.decode('utf-8')
            print("El cliente nos manda ", linea)
            (metodo, address, sip) = linea.split()
            if metodo == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n"
                                 + b"SIP/2.0 180 Ringing\r\n\r\n"
                                 + b"SIP/2.0 200 OK\r\n\r\n")
            elif metodo == 'ACK':
                # aEjecutar es un string
                # con lo que se ha de ejecutar en la shell
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            elif metodo == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif metodo != ('INVITE', 'ACK', 'BYE'):
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO = sys.argv[3]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 server.py IP port audio_file")
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
