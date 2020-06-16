# Shibabot

![Python](https://img.shields.io/badge/Python-v^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Discord](https://img.shields.io/badge/Discord-v1.0.1-blue.svg?longCache=true&logo=discord&style=flat-square&logoColor=white&colorB=B48EAD&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/network)

![Shibabot](https://github.com/toddbirchard/shibabot/blob/master/.github/shibabot@2x.png?raw=true)


## Installation

**Installation via `requirements.txt`**:

```shell
$ git clone https://github.com/toddbirchard/shibabot.git
$ cd shibabot
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ python3 main.py
```

**Installation via [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)**:

```shell
$ git clone https://github.com/toddbirchard/shibabot.git
$ cd shibabot
$ pipenv shell
$ pipenv update
$ python3 main.py
```

**Installation via [Poetry](https://python-poetry.org/)**:

```shell
$ git clone https://github.com/toddbirchard/shibabot.git
$ cd shibabot
$ poetry shell
$ poetry update
$ poetry run
```

## Usage

Replace the values in **.env.example** with your values and rename this file to **.env**:

* `ENVIRONMENT`: Set to either `development` or `production` for logging purposes.
* `DISCORD_TOKEN`: Secret API token.
* `DISCORD_GUILD`: Server names for bot to join.
* `GIPHY_API_KEY`: API key secret for fetching Giphy images.
* `IEX_API_TOKEN`: API key secret for fetching stock data.
* `ALPHA_VANTAGE_API`: API key secret for fetching crypto data.
* `PLOTLY_API_KEY`: Plotly chart studio API key.
* `PLOTLY_USERNAME`: Plotly user to generate charts via Plotly studio.

*Remember never to commit secrets saved in .env files to Github.*
