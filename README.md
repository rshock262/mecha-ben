# Baby's first discord bot
## Ben must transcend and leave humanity behind as a bot. Trapped forever in arguably his least favorite method of communication.

Following the docs: https://discordpy.readthedocs.io/en/latest/

```
pip install discord openai python-dotenv
```

## How to use

Run the bot using docker-compose:
```
docker-compose up --build
```

Run the bot using docker:
```
docker build -t discord_bot .
docker run -it discord_bot
```

Run the bot using python:
```
python3 ben.py
```
