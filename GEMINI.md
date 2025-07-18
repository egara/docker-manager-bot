# Project Summary
This project implements a Telegram bot in Python that allows managing Docker containers running on a server by sending specific messages to the bot.

# Programming Language
The project is developed in Python.

# Implemented Commands
- `/list`: Lists all running Docker containers.
- `/stop`: Stops a running Docker container. When this command is executed, a list of active containers will be presented for the user to select which one to stop.

# Basic Requirements

- Object-oriented programming best practices must be applied.
- Proper encapsulation.
- Good project structure. Each implemented class must be in its own file. Different classes should not be mixed in the same text file.
- This project must be deployed using Docker Compose on the server. Therefore, it will be necessary to create a Dockerfile for its construction and a docker-compose.yaml to deploy it.
- It is necessary to take into account that, as the bot runs inside a container, the Docker socket running on the host must be exposed inside the container itself because it will need to interact with all the host's containers.
- The code must be perfectly documented in English with comments that explain its functionality.
- Each time a Telegram command is executed, it must be logged, indicating the command and the user who executed it.