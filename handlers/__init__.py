"""Initiate handlers."""
import chart_studio

from config import (
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_CHART_BASE_URL,
    ALPHA_VANTAGE_PRICE_BASE_URL,
    IEX_API_BASE_URL,
    IEX_API_TOKEN,
    PLOTLY_API_KEY,
    PLOTLY_USERNAME,
)

from .crypto import CryptoChartHandler
from .stock import StockChartHandler

# Plotly chart studio authentication
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY
)

# Create handlers
stock_chart_handler = StockChartHandler(token=IEX_API_TOKEN, endpoint=IEX_API_BASE_URL)

crypto_chart_handler = CryptoChartHandler(
    token=ALPHA_VANTAGE_API_KEY,
    price_endpoint=ALPHA_VANTAGE_PRICE_BASE_URL,
    chart_endpoint=ALPHA_VANTAGE_CHART_BASE_URL,
)
