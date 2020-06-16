"""Chart creation."""
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
from .log import LOGGER
from config import (
    IEX_API_TOKEN,
    ALPHA_VANTAGE_API_KEY,
    PLOTLY_USERNAME,
    PLOTLY_API_KEY
)


# Authenticate with Plotly chart studio
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)


@LOGGER.catch
def crypto_plotly_chart(symbol):
    """Generate 30-day crypto price chart."""
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': 'USD',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    req = requests.get('https://www.alphavantage.co/query', params=params)
    data = req.json()
    df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')[:30]
    if df.empty is False:
        df = df.apply(pd.to_numeric)
        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df['1a. open (USD)'],
                high=df['2a. high (USD)'],
                low=df['3a. low (USD)'],
                close=df['4a. close (USD)'])
            ]
        )
        fig.update_layout(xaxis_rangeslider_visible=False, title=symbol)
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
def stock_price_chart(symbol, company):
    """Get 30-day stock chart."""
    params = {'token': IEX_API_TOKEN, 'includeToday': 'true'}
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1m/'
    req = requests.get(url, params=params)
    if req.status_code == 200:
        stock_df = pd.read_json(req.content)
        if stock_df.empty is False:
            fig = go.Figure(data=[
                go.Candlestick(
                    x=stock_df['date'],
                    open=stock_df['open'],
                    high=stock_df['high'],
                    low=stock_df['low'],
                    close=stock_df['close'])
                ]
            )
            fig.update_layout(xaxis_rangeslider_visible=False, title=f'30-day performance of {company}')
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
