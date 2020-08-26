"""Initiate handlers."""
import chart_studio
from .stock import StockChartHandler
from config import (
    PLOTLY_USERNAME,
    PLOTLY_API_KEY,
    IEX_API_BASE_URL,
    IEX_API_TOKEN
)


# Plotly chart studio authentication
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)

# Create handlers
stock_chart_handler = StockChartHandler(
    token=IEX_API_TOKEN,
    endpoint=IEX_API_BASE_URL
)

