import logging
import sys
import threading
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

    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s]: %(message)s'
    )
    logging.info("Initializing Event Horizon server...")

    listener_t = threading.Thread(target=listener, args=(HOST, PORT), daemon=True)
    listener_t.start()

    try:
        listener_t.join()
    except KeyboardInterrupt:
        logging.info("Exiting...")
