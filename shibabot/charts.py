"""Chart creation."""
from typing import Optional
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
from .log import LOGGER
from config import (
    IEX_API_TOKEN,
    IEX_API_BASE_URL,
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_CHART_BASE_URL,
    PLOTLY_USERNAME,
    PLOTLY_API_KEY
)


# Authenticate with Plotly chart studio
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)


@LOGGER.catch
def crypto_plotly_chart(symbol: str) -> Optional[str]:
    """Generate 60-day crypto price chart."""
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': 'USD',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    req = requests.get(ALPHA_VANTAGE_CHART_BASE_URL, params=params)
    data = req.json()
    df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')[:60]
    if df.empty is False:
        df = df.apply(pd.to_numeric)
        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df['1a. open (USD)'],
                high=df['2a. high (USD)'],
                low=df['3a. low (USD)'],
                close=df['4a. close (USD)'])
            ],
            layout=go.Layout(
                title=f'60-day performance of {symbol.upper()}',
                xaxis={
                    'type': 'date',
                    'rangeslider': {
                        'visible': False
                    },
                },

            )
        )
        chart = py.plot(
            fig,
            filename=symbol,
            auto_open=False,
            fileopt='overwrite',
            sharing='public'
        )
        chart_image = chart[:-1] + '.png'
        return chart_image
    return None


@LOGGER.catch
def stock_price_chart(symbol: str) -> Optional[str]:
    """Get 30-day stock chart."""
    params = {'token': IEX_API_TOKEN, 'includeToday': 'true'}
    url = f'{IEX_API_BASE_URL}{symbol}/chart/1m'
    req = requests.get(url, params=params)
    if req.status_code == 200:
        stock_df = pd.read_json(req.content)
        if stock_df.empty is False:
            stock_df = stock_df.loc[stock_df['date'].dt.dayofweek < 5]
            stock_df.set_index(keys=stock_df['date'], inplace=True)
            fig = go.Figure(data=[
                go.Candlestick(
                    x=stock_df.index,
                    open=stock_df['open'],
                    high=stock_df['high'],
                    low=stock_df['low'],
                    close=stock_df['close'],
                )],
                layout=go.Layout(
                    title=f'30-day performance of {symbol.upper()}',
                    xaxis={
                        'type': 'date',
                        'rangeslider': {
                            'visible': False
                        },
                    },
                )
            )
            chart = py.plot(
                fig,
                filename=symbol,
                auto_open=False,
                fileopt='overwrite',
                sharing='public'
            )
            chart_image = chart[:-1] + '.png'
            return chart_image
    return None

