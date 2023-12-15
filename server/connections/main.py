import logging
import socket
import socketserver
import threading

from server.crypto import decrypt


class Listener(socketserver.BaseRequestHandler):
    def handle(self):
        client_address = self.client_address
        logging.debug(f"Received a connection from {client_address[0]}:{client_address[1]}")

        # Send a welcome message to the client
        welcome_message = "Welcome to the server!\n"
        self.request.sendall(welcome_message.encode())

        # Handle data from the client
        while True:
            try:
                data = self.request.recv(1024)
            except ConnectionError:
                logging.debug(f"Connection to {client_address[0]}:{client_address[1]} lost!")
                return
            if not data:
                break  # Break the loop if no more data is received
            # print(f"Received from {client_address}: {data.decode()}")


def listener(host: str, port: int):
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer((host, port), Listener) as server:
            logging.info(f"Server is listening on {host}:{port}")
            server.serve_forever()
            server_thread.join()
    except KeyboardInterrupt:
        logger.info("Exiting...")
        server.shutdown()
