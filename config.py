from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

# Create graphs directory if it doesn't exist
os.makedirs('graphs', exist_ok=True)

EMAIL_CONFIG = {
    'smtp_server': getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(getenv('SMTP_PORT', '587')),
    'sender_email': getenv('SENDER_EMAIL'),
    'sender_password': getenv('SENDER_PASSWORD'),
    'recipient_email': getenv('RECIPIENT_EMAIL')
}

ASSETS = {
    'crypto': ['bitcoin', 'ethereum', 'cardano'],
    'stocks': {
        'period': '1mo',
        'AAPL': 'GOOGL',
        'MSFT': 'GOOGL'
    }
}