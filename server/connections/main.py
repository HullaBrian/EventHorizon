import socket
import socketserver
import threading


connections = []


class Listener(socketserver.BaseRequestHandler):
    def handle(self):
        global connections
        client_address = self.client_address
        print(f"[+] Server received a connection from {client_address}")

        try:
            with threading.Lock():
                connections.append(self.request)
                print("Connections: ")
                for connection in connections:
                    print("\t" + str(connection.getpeername()))
        except OSError:
            pass

        welcome_message = "Welcome to the server!"
        self.request.sendall(welcome_message.encode())

        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break  # Break the loop if no more data is received
                print(f"Data received from {client_address}:{data.decode()}")
        except ConnectionResetError:
            print(f"[-] Connection from {client_address} was reset.")
        except Exception as e:
            print(f"[-] Encountered an error while handling connection from {client_address}: {str(e)}")
        finally:
            self.request.close()


def listener(host: str, port: int):
    try:
        with socketserver.ThreadingTCPServer((host, port), Listener) as server:
            print(f"[+] Server is listening on {host}:{port}")
            server.serve_forever()
            server_thread.join()
    except KeyboardInterrupt:
        print("Exiting...")
        server.shutdown()
