import sys
from server.connections.main import listener


if __name__ == "__main__":
    HOST: str = "127.0.0.1"
    PORT: int = 61337
    for i, arg in enumerate(sys.argv):
        if arg in ["--host", "-h"]:
            try:
                HOST = sys.argv[i + 1]
            except IndexError:
                print("Invalid usage!")
        if arg in ["--port", "-p"]:
            try:
                PORT = int(sys.argv[i + 1])
            except IndexError:
                print("Invalid usage!")
            except ValueError:
                print("Port must be a number!")
    listener(HOST, PORT)
