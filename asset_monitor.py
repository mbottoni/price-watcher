from datetime import datetime, timedelta
import yfinance as yf
from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.graph_objects as go
from email_service import EmailService

class AssetMonitor:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.email_service = EmailService()
        
    def fetch_crypto_data(self, crypto_ids):
        """Fetch current and historical crypto data"""
        crypto_data = {}
        for crypto_id in crypto_ids:
            data = self.cg.get_coin_market_chart_by_id(
                id=crypto_id,
                vs_currency='usd',
                days=30
            )
            prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            crypto_data[crypto_id] = prices
        return crypto_data

    def fetch_stock_data(self, stock_symbols):
        """Fetch current and historical stock data"""
        stock_data = {}
        for symbol in stock_symbols:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='30d')
            stock_data[symbol] = data
        return stock_data

    def generate_graph(self, asset_data, asset_name):
        """Generate price graph using plotly"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=asset_data.index,
            y=asset_data['price'] if 'price' in asset_data else asset_data['Close'],
            name=asset_name
        ))
        fig.update_layout(title=f'{asset_name} 30-Day Price History')
        return fig

    def generate_daily_report(self, crypto_ids, stock_symbols):
        """Generate and send daily report"""
        # Fetch data
        crypto_data = self.fetch_crypto_data(crypto_ids)
        stock_data = self.fetch_stock_data(stock_symbols)
        
        # Generate graphs and prepare report
        report_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'assets': []
        }

        # Process crypto assets
        for crypto_id in crypto_data:
            current_price = crypto_data[crypto_id]['price'].iloc[-1]
            daily_change = ((current_price - crypto_data[crypto_id]['price'].iloc[-2]) / 
                          crypto_data[crypto_id]['price'].iloc[-2] * 100)
            
            graph = self.generate_graph(crypto_data[crypto_id], crypto_id)
            graph.write_image(f"graphs/{crypto_id}_graph.png")
            
            report_data['assets'].append({
                'name': crypto_id,
                'price': current_price,
                'daily_change': daily_change,
                'graph_path': f"graphs/{crypto_id}_graph.png"
            })

        # Process stock assets
        for symbol in stock_data:
            current_price = stock_data[symbol]['Close'].iloc[-1]
            daily_change = ((current_price - stock_data[symbol]['Close'].iloc[-2]) /
                          stock_data[symbol]['Close'].iloc[-2] * 100)
            
            graph = self.generate_graph(stock_data[symbol], symbol)
            graph.write_image(f"graphs/{symbol}_graph.png")
            
            report_data['assets'].append({
                'name': symbol,
                'price': current_price,
                'daily_change': daily_change,
                'graph_path': f"graphs/{symbol}_graph.png"
            })

        # Send email report
        self.email_service.send_daily_report(report_data)