import logging
import os
import sys
import threading
import subprocess
from server.connections.main import listener

HOST: str = "127.0.0.1"
PORT: int = 61337
AGENT_NAME: str = "gravity"

logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s]: %(message)s'
)


def parse_agent_cmd(call: list[str, ...]) -> None:
    global HOST, PORT

    for i, arg in enumerate(call):
        if arg in ["--host", "-h"]:
            try:
                HOST = call[i + 1]
            except IndexError:
                print("Invalid usage!")
        elif arg in ["--port", "-p"]:
            try:
                PORT = int(call[i + 1])
            except IndexError:
                print("Invalid usage!")
            except ValueError:
                print("Port must be a number!")
        elif arg in ["--name", "-n", "--output", "-o"]:
            AGENT_NAME = call[i + 1]
        else:
            if arg.startswith("-"):
                print(f"Unknown parameter '{arg}'")
                exit()

def build_agent():
    logging.info("Building agent...")
    cmd = f"gcc -Wall agent/linux/main.c agent/linux/syslog_aggregator.c -o {AGENT_NAME} -D LHOST=\"{HOST}\" -D PORT={PORT}"
    logging.debug(f"Running '{cmd}'")
    output = subprocess.check_output(cmd.split(), text=True)
    if AGENT_NAME in os.listdir():
        logging.info("Successfully generated agent!")
    else:
        print(output)
        logging.error("Agent generation failed!")


if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if arg in ["--host", "-h"]:
            try:
                HOST = sys.argv[i + 1]
            except IndexError:
                print("Invalid usage!")
        elif arg in ["--port", "-p"]:
            try:
                PORT = int(sys.argv[i + 1])
            except IndexError:
                print("Invalid usage!")
            except ValueError:
                print("Port must be a number!")
        elif arg in ["--generate-agent", "--generate", "-g"]:
            parse_agent_cmd(sys.argv[i + 1:])
            build_agent()
            exit()
        else:
            if arg.startswith("-"):
                print(f"Unknown parameter '{arg}'")
                exit()

    logging.info("Initializing Event Horizon server...")

    listener_t = threading.Thread(target=listener, args=(HOST, PORT), daemon=True)
    listener_t.start()

    try:
        listener_t.join()
    except KeyboardInterrupt:
        logging.info("Exiting...")
