# FakeMilo

FakeMilo is an educational discord bot where you can organise a tournament and compete with your friends to a battle of trivia questions.

<a href="https://hack36.com"> <img src="http://bit.ly/BuiltAtHack36" height=20px> </a>

## Features 

The features of the bot are split into 4 cogs (as of now) each of which caters to a set of commands and functionality.

The cogs used here are:

- <b>exe2</b> : Admin only command used to run code snippets without actually needing to modify the code. For on the go testing.
- <b>help</b> : Caters to ```m!help``` command.
- <b>player</b> : Handles the database queries and also shows highest scorers of all time.
- <b>quiz</b> : The main cog which handles the tournaments by creating brackets and conducts matches by fetching queries from the trivia API.

## Table Of Contents
- Technology Stacks
- Usage
- Installation
- Contributors

## Technology Stacks

- Python 3
- discord.py
- Mongo DB
- Trivia API

## Usage

- [Invite the bot to your server from the invite link](https://discordapp.com/oauth2/authorize?client_id=830132289010532372&scope=bot&permissions=603286592)
- Grant all the necessary permissions
- Type ``m!help`` to receive all the help you need with the bot.

Some of the common commands are as follows:
- ```m!help``` : guides the user on how to use other commands
- ```m!quiz <parameter1> <parameter2> ...``` : Creates match brackets and organise the tournament among the users provided
- ```m!match <match number>``` : Conducts matches according to tournament brackets.
- ```m!highest_scores``` : Returns the highest scorers of all time


## Installation

> If you want to run your own instance of the bot follow the following steps:

### Cloning the repository

Clone the repository using

```bash
    git clone https://github.com/embiway/FakeMilo.git
```

### Installing the required libraries and dependencies

Install the requirements using 

```bash
    pip install -r requirements.txt
```

### Setting up the environment variable

Create a ```.env``` file and add the following tokens

```bash
F_TOKEN=<Your bot token>
CONNECTION_URL=<Your mongodb cluster url>
```

### Starting the bot

Run the following

```bash
    python bot.py
```


### Contributors

Team Name : <b>br1cks</b>

- [Abhinav Koul](https://github.com/CodenameGHOST007)
- [Aryaman Arora]()
- [Mridul Bhatt](https://github.com/embiway)


<a href="https://hack36.com"> <img src="http://bit.ly/BuiltAtHack36" height=20px> </a>
