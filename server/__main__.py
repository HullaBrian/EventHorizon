"""
Event Horizon __main__.py
"""
import logging
import os
import sys
import threading
import subprocess

from base64 import b64encode, b64decode

from server.connections.main import listener, server
from server.crypto import rand_iv, rand_key, gen_uuid, padding
from server.db.manager import check_db, add_agent, connection

HOST: str = "127.0.0.1"
PORT: int = 61337
AGENT_NAME: str = "gravity"
db_cursor = None

logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s]: %(message)s'
)


def db_routine():
    """Routine to check the health of the database"""

    print("\n" + "-" * 20)
    logging.info("Checking database health...")
    db_cursor = check_db()
    print("-" * 20 + "\n")
    return db_cursor


def parse_agent_cmd(call: list[str, ...]) -> tuple[str, str, str]:
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
                sys.exit()
    return HOST, PORT, AGENT_NAME

def build_agent() -> None:
    """
    Build linux agent using command line parameters
    """
    uuid: str = gen_uuid()
    logging.info("Successfully generated UUID for agent!")
    key: str = b64encode(rand_key()).decode('utf-8').ljust(32)[:32].replace(" ", "-")
    logging.info("Successfully generated new encryption key!")
    iv: str = b64encode(rand_iv()).decode('utf-8').ljust(16)[:16].replace(" ", "-")
    logging.info("Successfully generated new IV!")

    print("\n" + "-" * 60)
    print(f"UUID: {uuid}")
    print(f"Encryption key: {key}")
    print(f"iv ({len(iv.encode('utf-8'))}): {iv}")
    print("-" * 60 + "\n")

    logging.info("Building agent...")
    # agent/linux/aes.c
    cmd = f"gcc -Wall agent/linux/main.c agent/linux/syslog_aggregator.c -o {AGENT_NAME}\
         -D LHOST=\"{HOST}\"\
         -D PORT={PORT}\
         -D IV=\"{iv}\"\
         -D KEY=\"{key}\"\
         -D UUID=\"{uuid}\"\
         -lcrypto -lssl"
    logging.info(f"Running '{cmd}'")
    output = subprocess.check_output(cmd.split(), text=True)
    if AGENT_NAME in os.listdir():
        logging.info("Successfully generated agent!")
    else:
        print(output)
        logging.error("Agent generation failed!")
        return

    logging.info("Adding agent information to agents database")
    try:
        add_agent(
            db_cursor,
            uuid=uuid,
            key=key,
            iv=iv
        )
    except AttributeError as e:
        logging.error("Couldn't add agent due to database not being initialized!")
        return


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
            db_cursor = db_routine()
            build_agent()
            sys.exit()
        else:
            if arg.startswith("-"):
                print(f"Unknown parameter '{arg}'")
                sys.exit()

    logging.info("Initializing Event Horizon server...")
    db_routine()

    listener_t = threading.Thread(target=listener, args=(HOST, PORT), daemon=True)
    listener_t.start()

    try:
        listener_t.join()
    except KeyboardInterrupt:
        logging.info("Exiting...")
        db_cursor.close()
