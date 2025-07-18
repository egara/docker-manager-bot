# Telegram Bot for Docker Management

This project implements a Python-based Telegram bot to manage Docker containers running on a server. It is a pet project
to test all the capabilities of [Gemini-CLI](https://github.com/google-gemini/gemini-cli). It pretends to be entirely build using this AI tool.

## Features

* List running Docker containers.
* Stop running Docker containers.

## Requirements

Due to this bot has been designed to live in a Docker container, those are the requirements needed to run it in
your own infrastructure:

* Docker
* Docker Compose

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/egara/docker-manager-bot.git
    cd telegram-bot-docker
    ```

2.  **Configure the Telegram Token:**
    - Open the `docker-compose.yaml` file.
    - Find the `environment` section for the `telegram-bot` service.
    - Replace `<YOUR_TELEGRAM_TOKEN>` with your actual Telegram bot token.

    ```yaml
    # docker-compose.yaml
    services:
      telegram-bot:
        environment:
          # --- Telegram Bot Token (Required) ---
          - TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN> # <-- REPLACE THIS
    ```

## Running the Bot

This bot can run in two modes: **Polling** and **Webhook**.

### Mode 1: Polling (Default)

In this mode, the bot actively asks Telegram for new messages. It's simple to set up and works without a public URL.

To build and run the bot in Polling mode, simply run:

```bash
docker-compose up --build
```

### Mode 2: Webhook (Advanced)

In this mode, Telegram sends updates directly to your bot via a public URL. This is more efficient and recommended for production.

**Requirements for Webhook Mode:**

*   A public URL from a service like [ngrok](https://ngrok.com/).

**Setup for Webhook Mode:**

1.  **Get a public URL:**
    Start ngrok to forward traffic to the port you will use (e.g., 8443):
    ```bash
    ngrok http 8443
    ```
    ngrok will give you a public HTTPS URL, like `https://1a2b-3c4d-5e6f.ngrok.io`.

2.  **Configure `docker-compose.yaml`:**
    - In your `docker-compose.yaml` file, add the `USE_WEBHOOK`, `PUBLIC_URL`, and `PORT` environment variables and expose the port.

    ```yaml
    # docker-compose.yaml
    version: '3.8'
    services:
      telegram-bot:
        build: .
        environment:
          # --- Telegram Bot Token (Required) ---
          - TELEGRAM_TOKEN=<YOUR_TELEGRAM_TOKEN> # <-- REPLACE THIS

          # --- Webhook Configuration (Optional) ---
          - USE_WEBHOOK=true
          - PUBLIC_URL=https://1a2b-3c4d-5e6f.ngrok.io # <-- REPLACE THIS
          - PORT=8443
        ports:
          - "8443:8443"
    ```

3.  **Run Docker Compose:**
    ```bash
    docker-compose up --build
    ```

## Usage

Once the bot is running, you can interact with it through your Telegram client.

*   **List running containers:**
    Send the `/list` command to the bot. It will reply with a list of all currently running Docker containers on the host machine.
*   **Stop running containers:**
    Send the `/stop` command to the bot. It will reply with a list of all currently running Docker containers on the host machine. Select the one you want to stop.

## Deployment

This repository is configured with GitHub Actions to automatically build and push the Docker image to [Docker Hub](https://hub.docker.com/r/egarcia/docker-manager-bot) upon every push to the `main` branch.

Two tags are created for each push:
- `latest`: Always points to the most recent build.
- `YYYYMMDD`: A tag with the date of the build (e.g., `20250718`).

### Running in Production

For production environments, it's recommended to use the pre-built image from Docker Hub. A `docker-compose.prod.yaml` file is provided for this. It pulls the `egarcia/docker-manager-bot:latest` image.

**Setup:**

1.  Ensure you have a `docker-compose.prod.yaml` file.
2.  Configure your Telegram Token in `docker-compose.prod.yaml` as described in the "Setup" section. You can also configure the webhook settings here if needed.

**Command:**

To run the bot using the production image, execute:
```bash
docker-compose -f docker-compose.prod.yaml up -d
```
This command will download the latest image from Docker Hub and start the bot in detached mode.