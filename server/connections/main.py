import socket
import socketserver
import threading


class Listener(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print(data)
        socket = self.request[1]
        current_thread = threading.current_thread()
        print(f"[{self.client_address[0]}:{self.client_address[0]}]: {data.decode('utf-8')}")
        socket.sendto(data.upper(), self.client_address)


def listener(host: str, port: int):
    try:
        with socketserver.ThreadingUDPServer((host, port), Listener) as server:
            print(f"[+] Server is listening on {host}:{port}")
            server.serve_forever()
            server_thread.join()
    except KeyboardInterrupt:
        print("Exiting...")
        server.shutdown()
