![Logo](assets/EventHorizon.svg)
# EventHorizon
EventHorizon will eventually become a Security Information and Event Management (SIEM) system.

# Server
## Pre-Installation / Dependencies
- The server requires that you have python installed
- In order to compile agents yourself you need go installed

## Installation
- Server installation documentation coming soon...
## Starting
- To start the server, run:
```
python3 -m server -h <server ip> -p <port>
```
- While you don't have to provide an ip or port, the server by default listens on `127.0.0.1:61337`

# Agents
## Generating an Enrollment Key
- To generate an agent, run the server (see the server starting section)
- Use the `generate` command to create an enrollment key
## Installation
- Run the agent on the machine you want to install the agent on, and provide an enrollment key to it.
## Security
- The agent, by default, uses `AES-256` encryption. The only plaintext traffic it will send is its hardcoded uuid which allows the server to lookup the necessary encryption key/IV
