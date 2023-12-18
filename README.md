![Logo](assets/EventHorizon.svg)
# EventHorizon
"You can't escape the Event Horizon"

EventHorizon will eventually become a Security Information and Event Management (SIEM) system.
Right now, it simply aggregates syslog logs and prints them to the server's terminal. <u>This will change</u>


# Server
## Installation
- Server installation documentation coming soon...
## Starting
- To start the server, run:
```
python3 -m server -h <server ip> -p <port>
```
- While you don't have to provide an ip or port, the server by default listens on `127.0.0.1:61337`

# Agents
## Generation
- To generate an agent, run:
```
python3 -m server -g -h <server ip> -p <server port>
```
- While you don't have to provide an ip or port, the agents attempts to connect to `127.0.0.1:61337`


- Event Horizon will generate an agent and add a uuid, encryption key, and initialization vector to its internal `agents.db`
 database
- To run the agent, run:
```
./gravity
```
## Functionality
- In order for the agent to function properly (for now) you'll have to ensure that rsyslog is installed on the agent machine
and configure it to send logs on the port it connects to the server on + 1. So if you set the agent to connect to the server
 on port 61337, configure rsyslog to send logs to `127.0.0.1:61338`
## Security
- The agent, by default, uses OpenSSL's `AES-256-CTR` encryption. The only plaintext traffic it will send is its hardcoded uuid which 
which allows the server to lookup the necessary encryption key/IV

# Known Issues
- Sometimes the agent exits unexpectedly after only a short period of log aggregation
- The server periodically receives traffic from an agent that cannot decrypt properly