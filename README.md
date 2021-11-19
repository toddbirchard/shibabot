# Shibabot

![Shibabot](./.github/shibabot_small@2x.png)

![Python](https://img.shields.io/badge/Python-v^3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Discord](https://img.shields.io/badge/Discord-v1.7.3-blue.svg?longCache=true&logo=discord&style=flat-square&logoColor=white&colorB=B48EAD&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/shibabot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/shibabot/network)

## Commands

* `!giphy [param]`: Fetch a gif from Giphy.
* `!stock [param]`: 30-day performance chart for a given stock ticker symbol.
* `!crypto [param]`: 60-day performance chart for a given cryptocurrency symbol.
* `!wiki [param]`: Fetch Wikipedia summary of a given topic.
* `!imdb [param]`: Fetch movie summaries, ratings, and box office performance.
* `!urban [param]`: Get definition from UrbanDictionary.
* `!weather [param]`: Return temperature and weather per city/state/zip.

## Getting Started

### Installation

Install and run this bot via simple Makefile commands:

```shell
$ git clone https://github.com/toddbirchard/shibabot.git
$ cd shibabot
$ make install
$ make run
```

### Configuration

Replace the values in **.env.example** with your values and rename this file to **.env**:

* `ENVIRONMENT`: Set to either `development` or `production` for logging purposes.
* `DISCORD_TOKEN`: Secret API token.
* `DISCORD_CHANNEL_1`: Server name for bot to join.
* `DISCORD_CHANNEL_2`: Additional server name for bot to join (optional).
* `GIPHY_API_KEY`: API key secret for fetching Giphy images.
* `IEX_API_TOKEN`: API key secret for fetching stock data.
* `ALPHA_VANTAGE_API`: API key secret for fetching crypto data.
* `PLOTLY_API_KEY`: Plotly chart studio API key.
* `PLOTLY_USERNAME`: Plotly user to generate charts via Plotly studio.
* `WEATHERSTACK_API_KEY`: API key for fetching weather data.

*Remember never to commit secrets saved in .env files to Github.*
