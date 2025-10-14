import os

class Config:
    SECRET_KEY = 'picknpay-analytics-secret-key'
    DATABASE = 'database/picknpay.db'
    SQL_FILE = 'database/picknpay.sql'
    ANALYTICS_PERIOD = '7d'
    EXCHANGE_RATE = 1.0  # Changed to 1.0 since we're using USD directly
    USE_SQL_FILE = False
    UPLOAD_FOLDER = 'database/uploads'
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 100MB max file size

# Create uploads directory
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)