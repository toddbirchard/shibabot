"""Create cloud-hosted Candlestick charts of company stock data."""
from typing import Optional
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py


class StockChartHandler:
    """Create chart from stock market data."""

    def __init__(self, token: str, endpoint: str):
        self.token = token
        self.endpoint = endpoint

    def _chart_raw_data(self, symbol: str) -> Optional[dict]:
        """Fetch 30-day performance data from API."""
        params = {'token': self.token, 'includeToday': 'true'}
        url = f'{self.endpoint}{symbol}/chart/1m'
        req = requests.get(url, params=params)
        if req.status_code == 200:
            return req.json()
        return None

    def _chart_data(self, symbol) -> Optional[pd.DataFrame]:
        """Parse price data JSON into Pandas DataFrame."""
        data = self._chart_raw_data(symbol)
        stock_df = pd.read_json(data)
        if stock_df.empty is False:
            stock_df = stock_df.loc[stock_df['date'].dt.dayofweek < 5]
            stock_df.set_index(keys=stock_df['date'], inplace=True)
            return stock_df
        return None

    def create_chart(self, symbol: str) -> Optional[str]:
        """Create chart of a company's 30-day stock performance."""
        stock_df = self._chart_data(symbol)
        if stock_df:
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
