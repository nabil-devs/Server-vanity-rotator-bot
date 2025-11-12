

# Server Vanity Rotator Bot (Educational Version)

**Disclaimer:** This project is strictly for **educational purposes only**.
Do **not** use this bot on servers you do not own or have explicit permission to modify.
Abusing this code may violate Discord's Terms of Service and could result in account termination.

---

## Overview

This project demonstrates how to structure a Discord bot/selfbot for learning purposes.
It includes:

* Dynamic configuration using `.env`
* Logging actions in the terminal and optionally via webhook
* Version tracking for the bot

**Important:** This code is intended to **teach Python, Discord API interactions, and bot structure**, not to manipulate servers without permission.

---

## Features (Educational)

* Loads settings from `.env` file
* Tracks bot version
* Logs actions with timestamps to terminal
* Optional: Send logs to a Discord webhook

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nabil-devs/Server-vanity-rotator-bot
cd Server-vanity-rotator-bot
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the bot:

```bash
python main.py
```

Terminal will show logs including the bot version and actions being taken (for educational purposes).

---

## Version

Current version: `1.0.0`

---

## License

MIT License

