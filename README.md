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
Discord guild.

```bash
# Your dotenv file should look similar to this
# The .env file will need to live in your home directory
DISCORD_TOKEN={your-bot-token}
DISCORD_GUILD={your-guild-name}
```

Upon running:
```bash
pipenv shell
py __main__.py
```
The client should properly establish a connection.

***
TODO
- [x] Allow users to only use the access command once every 60-120 seconds
- [x] We will need cooldown timers for each command that wants to call a timer
- [x] Allow access command to get the member role and provide role specific token/info
- [x] Figure out the best way to provide oauth access (maybe a token that contains the entire state + member or maybe do things via IP addr)
