# oauth-file-bot
A discord bot for providing oauth tokens to client members

## Installation
This project utilizes pipenv for ease of installation.
After cloning the project:
```bash
cd oauth-file-bot
# Simple install
pipenv install
# Dev install (with linter, etc.)
pipenv install --dev
```

## Note:
In order to run the CustomClient, a python-dotenv is necessary. The
dotenv will need to contain the client secret along with the appropriate
Discord guild

```bash
# Your dotenv file should look similar to this
# The .env file will need to live in your home directory
DISCORD_TOKEN={your-bot-token}
DISCORD_GUILD={your-guild-name}
```

Upon running:
```bash
py bot.py
```
The client should properly connect to the guild
