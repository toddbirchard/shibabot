"""Cloud-hosted Candlestick charts of crypto performance."""
from datetime import datetime
from typing import Optional

import chart_studio.plotly as py
import pandas as pd
import plotly.graph_objects as go
import requests
from requests.exceptions import HTTPError

from log import LOGGER


class CryptoChartHandler:
    """Create chart from stock market data."""

    def __init__(self, token: str, price_endpoint: str, chart_endpoint: str):
        self.token = token
        self.price_endpoint = price_endpoint
        self.chart_endpoint = chart_endpoint

    def get_chart(self, symbol: str) -> str:
        """Get crypto data and generate Plotly chart."""
        message = self._get_price(symbol)
        chart = self._create_chart(symbol)
        if message and chart:
            return f"{message} {chart}"
        return "dats nought a stock symbol u RETART :@"

    def _get_price(self, symbol: str) -> Optional[str]:
        """Get crypto price for provided ticker label."""
        endpoint = f"{self.price_endpoint}{symbol.lower()}usd/summary"
        try:
            req = requests.get(url=endpoint)
            prices = req.json()["result"]["price"]
            percentage = prices["change"]["percentage"] * 100
            if prices["last"] > 1:
                return (
                    f'{symbol.upper()}: Currently at ${prices["last"]:.2f}. '
                    f'HIGH today of ${prices["high"]:.2f}, LOW of ${prices["low"]:.2f} '
                    f"(change of {percentage:.2f}%)."
                )
            else:
                return (
                    f'{symbol.upper()}: Currently at ${prices["last"]}. '
                    f'HIGH today of ${prices["high"]} LOW of ${prices["low"]} '
                    f"(change of {percentage:.2f}%)."
                )
        except HTTPError as e:
            LOGGER.error(
                f"Failed to fetch crypto price for `{symbol}`: {e.response.content}"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error when fetching crypto price for `{symbol}`: {e}"
            )

    def _get_chart_data(self, symbol: str) -> Optional[dict]:
        """Fetch 60-day crypto prices."""
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
            "apikey": self.token,
        }
        try:
            req = requests.get(self.chart_endpoint, params=params)
            if req.status_code == 200 and req.json():
                return req.json()
        except HTTPError as e:
            LOGGER.error(
                f"Failed to fetch crypto data for `{symbol}`: {e.response.content}"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error when fetching crypto data for `{symbol}`: {e}"
            )

    @staticmethod
    def _parse_chart_data(data: dict) -> Optional[pd.DataFrame]:
        """Parse JSON response into Pandas DataFrame"""
        return pd.DataFrame.from_dict(
            data["Time Series (Digital Currency Daily)"], orient="index"
        )[:60]

    @LOGGER.catch
    def _create_chart(self, symbol: str) -> Optional[str]:
        """Create Plotly chart for given crypto symbol."""
        data = self._get_chart_data(symbol)
        if bool(data):
            crypto_df = self._parse_chart_data(data)
            crypto_df = crypto_df.apply(pd.to_numeric)
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=crypto_df.index,
                        open=crypto_df["1a. open (USD)"],
                        high=crypto_df["2a. high (USD)"],
                        low=crypto_df["3a. low (USD)"],
                        close=crypto_df["4a. close (USD)"],
                        decreasing={
                            "line": {"color": "rgb(240, 99, 90)"},
                            "fillcolor": "rgba(142, 53, 47, 0.5)",
                        },
                        increasing={
                            "line": {"color": "rgb(48, 190, 161)"},
                            "fillcolor": "rgba(22, 155, 124, 0.6)",
                        },
                        whiskerwidth=1,
                    )
                ],
                layout=go.Layout(
                    font={"size": 15, "family": "Open Sans", "color": "#fff"},
                    title={
                        "x": 0.5,
                        "font": {"size": 23},
                        "text": f"30-day performance of {symbol.upper()}",
                    },
                    xaxis={
                        "type": "date",
                        "rangeslider": {"visible": False},
                        "ticks": "",
                        "gridcolor": "#283442",
                        "linecolor": "#506784",
                        "automargin": True,
                        "zerolinecolor": "#283442",
                        "zerolinewidth": 2,
                    },
                    yaxis={
                        "ticks": "",
                        "gridcolor": "#283442",
                        "linecolor": "#506784",
                        "automargin": True,
                        "zerolinecolor": "#283442",
                        "zerolinewidth": 2,
                    },
                    autosize=True,
                    plot_bgcolor="rgb(23, 27, 31)",
                    paper_bgcolor="rgb(23, 27, 31)",
                ),
            )
            chart = py.plot(
                fig,
                filename=f'{symbol}_{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}',
                auto_open=False,
                fileopt="overwrite",
                sharing="public",
            )
            chart_image = chart[:-1] + ".png"
            return chart_image
