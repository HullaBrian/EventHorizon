import logging
import sqlite3

from pathlib import Path

agents_db: str = "agents.db"
connection: sqlite3.Connection = None


def check_db():
    """
    Checks agents.db to make sure that it exists
    """
    global connection
    logging.info("Performing health check on database.")

    path = Path(agents_db)
    cursor = None
    if not path.is_file():
        logging.critical(f"No database called '{agents_db}' present for agent history!")

        logging.info("Creating new database to compensate")
        with open(agents_db, "w+", encoding="utf-8") as db:
            pass
        logging.info(f"Successfully created a new database called '{agents_db}'")
        init_agents_db()
    else:
        connection = sqlite3.connect(agents_db)
        cursor = connection.cursor()
        logging.info("Connected to database!")

    # More checks to come in the future...
    logging.info("Finished database health checks!\n")
    return cursor


def init_agents_db() -> sqlite3.Cursor:
    """
    Creates and initializes the database
    """
    global connection
    logging.warning("Initializing agent database. DO NOT STOP THIS PROCESS!")
    try:
        connection = sqlite3.connect(agents_db)
        cursor = connection.cursor()
        logging.info("Connected to database!")

        logging.debug("Adding agents table")
        query = "CREATE TABLE agents ( uuid TEXT NOT NULL, key TEXT NOT NULL, iv TEXT NOT NULL );"
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        logging.error(f"SQLite Error: {str(e)}")
    finally:
        if connection:
            connection.close()
            logging.debug('SQLite Connection closed')
    return cursor


def add_agent(cursor: sqlite3.Cursor, uuid: str, key: str, iv: str) -> bool:
    """
    Adds an agent to agents.db
    """
    query = f"INSERT INTO agents (uuid, key, iv) VALUES ('{uuid}', '{key}', '{iv}')"
    logging.debug(query)
    cursor.execute(query)
    connection.commit()
    return True


def lookup_by_uuid(uuid: str) -> tuple[str, str]:
    """
    Returns the encryption key and iv for a uuid
    """
    query = f"SELECT * FROM agents WHERE trim(UUID) LIKE '{uuid}';"
    logging.debug(query)
    match = sqlite3.connect(agents_db).execute(query).fetchall()

    if len(match) == 0:
        return ("", "")
    if len(match) > 1:
        logging.critical("Database contains multiple entries for this uuid! Is it corrupted?")
        return ("ERROR", "ERROR")

    return match[0][1:]
