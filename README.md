# Pick n Pay Advanced Analytics System

## Overview
A retail analytics platform for Pick n Pay with multi-store support and separate analytics pages. The system captures, cleans, and analyzes transaction data to provide actionable business insights.

## Features
- Multi-store database upload system
- Separate pages for each analytics section
- Sales trends analysis and forecasting
- Customer segmentation (including RFM analysis)
- Top products tracking
- Store performance metrics
- Interactive dashboards with dynamic charts
- Data cleaning and preprocessing (duplicate removal, missing value handling, normalization)
- Predictive modeling (sales forecasting, churn detection)
- Loyalty and demographic enrichment

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd project
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv .venv
   ```

3. **Activate the environment:**
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```sh
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Initialize the sample database:**
   ```sh
   python init_db.py
   ```

6. **Run the application:**
   ```sh
   python app.py
   ```

## Usage

1. Login with credentials:  
   **Username:** `admin`  
   **Password:** `admin123`

2. Select a store (1-5) from the dashboard.

3. Upload your SQLite database file (see schema below).

4. Navigate through the analytics pages:
   - Sales Trends
   - Customer Segmentation
   - Top Products
   - Store Performance

## Database Schema

Your SQLite database should contain the following tables and recommended columns:

- **transactions**
  - `id` (INTEGER, PRIMARY KEY)
  - `customer_id` (INTEGER)
  - `date` (TEXT, format: YYYY-MM-DD)
  - `total_amount` (REAL)
  - `store_id` (INTEGER)
- **customers**
  - `id` (INTEGER, PRIMARY KEY)
  - `name` (TEXT)
  - `gender` (TEXT)
  - `age` (INTEGER)
  - `loyalty_id` (TEXT)
- **products**
  - `id` (INTEGER, PRIMARY KEY)
  - `name` (TEXT)
  - `category` (TEXT)
  - `price` (REAL)
- **transaction_items**
  - `id` (INTEGER, PRIMARY KEY)
  - `transaction_id` (INTEGER)
  - `product_id` (INTEGER)
  - `quantity` (INTEGER)
  - `price` (REAL)

> **Note:** You can use `init_db.py` to generate a sample database with the correct schema.

## Requirements

- Python 3.8 or higher
- See `requirements.txt` for Python package dependencies

## Support

For issues or questions, please contact the project maintainer.
