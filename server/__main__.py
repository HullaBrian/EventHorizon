"""
Event Horizon __main__.py
"""
import logging
import os
import sys
import time
import threading
import subprocess

from base64 import b64encode, b64decode

from server.connections.main import listener
from server.crypto import rand_iv, rand_key, gen_uuid
from server.db.manager import check_db, add_agent, connection

HOST: str = "127.0.0.1"
PORT: int = 61337
AGENT_NAME: str = "gravity"
db_cursor = None
status: threading.Event = threading.Event()

logging.basicConfig(
        level=logging.DEBUG,
        format='\n[%(levelname)s]: %(message)s',
)
logging.StreamHandler.terminator = ""


def db_routine():
    """Routine to check the health of the database"""

    print("\n" + "-" * 20, end="")
    logging.info("Checking database health...")
    db_cursor = check_db()
    print("-" * 20, end="", flush=True)
    return db_cursor


def gen_agent_key() -> None:
    uuid: str = gen_uuid()
    key: str = b64encode(rand_key()).decode('utf-8').ljust(32)[:32].replace(" ", "-")
    iv: str = b64encode(rand_iv()).decode('utf-8').ljust(16)[:16].replace(" ", "-")
    agent_key: str = uuid + key + iv
    print( \
    f"""The agent's key has been generated. When setting up the new agent, use this as its key parameter.
Further details will be provided in time, but for now refer to the agent's source code to determine what parameter to use.    

    Key: {agent_key}

This session will continue until you enter "1" - with any other input cancelling the key to be added to the agent database.
""")
    choice = input()
    if choice == "1":
        logging.debug("")
    else:
        print("\nExiting...\n")


def shell () -> None:
    global HOST, PORT

    logging.debug("Started interactive debug shell\n\n")

    c: str = ""
    while c != "exit":
        confirm: str = "n"
        c = input("Event> ")
        
        match c:
            case "generate":
                print("Please confirm the configuration:")
                print(f"\tServer IP: {HOST}")
                print(f"\tServer Port: {PORT}")

                while confirm == "n":
                    confirm = input("Use this configuration? [Y/n] ").lower()
                    if confirm == "n":
                        try: 
                            HOST = input("Desired server IP address: ")
                            PORT = int(input("Desired server port: "))
                        except Exception as e:
                            print("Invalid configuration given. Please try again!\n")
                    logging.info("Successfully set the desired agent configuration!\n")
                logging.info("Generating agent configuration key...")
                logging.debug("DONE!\n")
            case "":
                pass
            case "exit":
                break
            case _:
                print("Help Menu:")
                print("\t{0:10s}\tPrints this menu".format("help"))
                print("\t{0:10s}\tGenerate an agent with specified host and port parameters.".format("generate"))
                print("\t{0:10s}\tExits the server".format("exit"))
                print()


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
        else:
            if arg.startswith("-"):
                print(f"Unknown parameter '{arg}'")
                sys.exit()

    logging.info("Initializing Event Horizon server...")
    logging.info("Checking agent database...")
    db_cursor = db_routine()
    logging.debug("Database check done!")

    logging.info("Initializing Agent listener...")
    listener_t = threading.Thread(target=listener, args=(HOST, PORT, status), daemon=True)
    listener_t.start()
    logging.debug("Initialized Agent listener!")

    while status.is_set() == False:  # Wait for socket server
        time.sleep(0.1)
    logging.info("Starting interactive debug shell...")
    try:
        shell()
        logging.debug("Stoped interactive debug shell")
    except KeyboardInterrupt:
        db_cursor.close()
    logging.info("Exiting...\n")
