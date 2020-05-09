# Shibabot

![Python](https://img.shields.io/badge/Python-v3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Discord](https://img.shields.io/badge/Discord-v1.0.1-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=B48EAD&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/network)


## Installation

**Installation via `requirements.txt`**:

```shell
$ git clone https://github.com/hackersandslackers/shibabot.git
$ cd shibabot
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ flask run
```

**Installation via [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)**:

```shell
$ git clone https://github.com/hackersandslackers/shibabot.git
$ cd shibabot
$ pipenv shell
$ pipenv update
$ flask run
```

## Configuration

Configuration is handled by creating a **.env** file. This should contain the following variables (replace the values with your own):

```.env
DISCORD_TOKEN="your_discord_token"
GIPHY_API_KEY="your_giphy_token"
```
