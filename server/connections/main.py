import logging
import socket
import socketserver
import threading

from base64 import b64encode

from server.crypto import decrypt
from server.db.manager import lookup_by_uuid

server: socketserver.ThreadingTCPServer = None


class Listener(socketserver.BaseRequestHandler):
    def handle(self):
        client_address = self.client_address

        uuid: str = self.request.recv(1024).decode()
        logging.info(f"Received a connection from {client_address[0]}:{client_address[1]} with uuid={uuid}")
        key, iv = lookup_by_uuid(uuid)
        iv = iv.encode("utf-8")
        key = key.encode("utf-8")
        o_len = 0

        while True:
            data: bytes | str = ""
            try:
                data = self.request.recv(1024)
                o_len = len(data)
                data = decrypt(iv, data, key).decode()
            except ConnectionError:
                logging.error(f"Connection to {client_address[0]}:{client_address[1]} lost due to connection error!")
                return
            except UnicodeDecodeError:
                logging.debug(f"Could not decrypt message from agent {client_address[0]}:{client_address[1]}! Received: {data}")
                return
            
            if not data:
                print("Received nothing. Closing connection...")
                break  # Break the loop if no more data is received
            print(f"Received {o_len} bytes from {client_address}: {data}")


def listener(host: str, port: int):
    global server
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer((host, port), Listener) as server:
            logging.info(f"Server is listening on {host}:{port}")
            server.serve_forever()
            server_thread.join()
    except KeyboardInterrupt:
        logger.info("Exiting...")
