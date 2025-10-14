from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
from functools import wraps
import sqlite3
import numpy as np
import os
import uuid
from datetime import datetime, timedelta
from config import Config
from utils.database_utils import get_database_connection
from utils.helpers import get_date_filter
from utils.pdf_generator import PDFReportGenerator
from utils.analytics import (
    clean_and_standardize, scale_numeric, detect_anomalies,
    feature_engineering, rfm_segmentation, kmeans_clustering,
    hierarchical_clustering, recommend_products
)
import pandas as pd
import tempfile

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def database_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'current_db' not in session or not os.path.exists(session['current_db']):
            return redirect(url_for('store_selection'))
        return f(*args, **kwargs)
    return decorated_function

def query_user_db(query, args=(), one=False):
    """Query the user's uploaded database"""
    if 'current_db' not in session:
        print("❌ No current_db in session")
        return None
    
    db_path = session['current_db']
    print(f"🔍 Querying database: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Database file does not exist: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print(f"📊 Executing query: {query}")
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.close()
        print(f"✅ Query returned {len(rv)} rows")
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        print(f"❌ Database query error: {e}")
        return None

def simple_forecast(values, periods=7):
    if len(values) < 2:
        return values
    
    x = np.arange(len(values))
    y = np.array(values)
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    future_x = np.arange(len(values), len(values) + periods)
    forecast_values = m * future_x + c
    return forecast_values.tolist()

@app.route('/')
@login_required
def index():
    if 'current_db' in session and os.path.exists(session['current_db']):
        return redirect(url_for('sales_trends'))
    return redirect(url_for('store_selection'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple authentication (replace with proper auth in production)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('store_selection'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/store-selection')
@login_required
def store_selection():
    return render_template('store_selection.html')

@app.route('/upload-database/<store_name>', methods=['GET', 'POST'])
@login_required
def upload_database(store_name):
    # Map store names to display names
    store_display_names = {
        'chikanga': 'Chikanga',
        'sakubva': 'Sakubva', 
        'town': 'Town',
        'dnangamvura': 'Dangamvura'
    }
    
    display_name = store_display_names.get(store_name, store_name)
    
    if request.method == 'POST':
        if 'database_file' not in request.files:
            return render_template('upload_database.html', store_name=store_name, display_name=display_name, error='No file selected')
        
        file = request.files['database_file']
        if file.filename == '':
            return render_template('upload_database.html', store_name=store_name, display_name=display_name, error='No file selected')
        
        if file and file.filename.endswith('.db'):
            filename = f"store_{store_name}_{uuid.uuid4().hex}.db"
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Verify it's a valid SQLite database
            try:
                conn = sqlite3.connect(filepath)
                conn.execute('SELECT 1')
                conn.close()
                
                session['current_db'] = filepath
                session['current_store'] = display_name  # Store display name
                session['store_identifier'] = store_name  # Store identifier for URLs
                print(f"✅ Database uploaded for {display_name} store: {filepath}")
                return redirect(url_for('sales_trends'))
            except sqlite3.Error as e:
                os.remove(filepath)
                print(f"❌ Invalid database file: {e}")
                return render_template('upload_database.html', store_name=store_name, display_name=display_name, error='Invalid database file')
    
    return render_template('upload_database.html', store_name=store_name, display_name=display_name)

@app.route('/sales-trends')
@login_required
@database_required
def sales_trends():
    print("📈 Loading sales trends page")
    return render_template('sales_trends.html')

@app.route('/customer-segments')
@login_required
@database_required
def customer_segments():
    print("👥 Loading customer segments page")
    return render_template('customer_segments.html')

@app.route('/top-products')
@login_required
@database_required
def top_products():
    print("🏆 Loading top products page")
    return render_template('top_products.html')

@app.route('/store-performance')
@login_required
@database_required
def store_performance():
    print("📊 Loading store performance page")
    return render_template('store_performance.html')

@app.route('/dashboard')
@login_required
@database_required
def dashboard():
    if 'current_db' not in session:
        return redirect(url_for('upload_database', store_name=session.get('store_identifier', '')))
    db_path = session['current_db']
    conn = sqlite3.connect(db_path)
    dfs = {}
    for table in ['transactions', 'customers', 'products', 'transaction_items']:
        try:
            dfs[table] = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        except Exception:
            dfs[table] = pd.DataFrame()
    conn.close()
    for k in dfs:
        dfs[k] = clean_and_standardize(dfs[k])
        dfs[k] = scale_numeric(dfs[k])
    dfs['transactions'] = detect_anomalies(dfs['transactions'])
    features = feature_engineering(dfs)
    rfm = rfm_segmentation(dfs['transactions'])
    features = kmeans_clustering(features)
    features = hierarchical_clustering(features)
    # Example: recommend for first customer if exists
    if not features.empty:
        recommendations = recommend_products(
            features['customer_id'].iloc[0],
            dfs['transactions'], dfs['transaction_items'], dfs['products']
        )
    else:
        recommendations = []
    # Pass all analytics to template
    return render_template(
        'dashboard.html',
        features=features.to_dict(orient='records'),
        rfm=rfm.to_dict(orient='index'),
        recommendations=recommendations
    )

# API Routes
@app.route('/api/sales-data')
@login_required
@database_required
def api_sales_data():
    period = request.args.get('period', '60d')
    date_filter = get_date_filter(period)
    print(f"📊 API Sales Data called with period: {period}")
    
    query = f'''
        SELECT date(timestamp) as day, SUM(total_amount) as total
        FROM Transactions
        WHERE date(timestamp) >= {date_filter}
        GROUP BY day
        ORDER BY day
    '''
    
    try:
        data = query_user_db(query)
        print(f"📊 Sales data query returned: {len(data) if data else 0} rows")
        
        if not data:
            return jsonify({
                'dates': [],
                'actual': [],
                'forecast': []
            })
            
        dates = [row['day'] for row in data]
        actual_values = [float(row['total']) for row in data]
        
        print(f"📊 Dates: {dates[:5]}...")  # Show first 5 dates
        print(f"📊 Values: {actual_values[:5]}...")  # Show first 5 values
        
        if len(actual_values) > 1:
            forecast_values = simple_forecast(actual_values, periods=7)
            forecast_for_dates = forecast_values[:len(actual_values)]
        else:
            forecast_for_dates = actual_values
        
        return jsonify({
            'dates': dates,
            'actual': actual_values,
            'forecast': forecast_for_dates
        })
    except Exception as e:
        print(f"❌ Error in api_sales_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer-segments')
@login_required
@database_required
def api_customer_segments():
    period = request.args.get('period', '60d')
    date_filter = get_date_filter(period)
    print(f"👥 API Customer Segments called with period: {period}")
    
    query = f'''
        SELECT 
            CASE 
                WHEN frequency > 10 AND monetary > 5000 THEN 'Platinum'
                WHEN frequency > 5 AND monetary > 2000 THEN 'Gold'
                WHEN frequency > 2 THEN 'Silver'
                ELSE 'Bronze'
            END as segment,
            COUNT(*) as count
        FROM (
            SELECT 
                customer_id,
                COUNT(*) as frequency,
                SUM(total_amount) as monetary
            FROM Transactions
            WHERE date(timestamp) >= {date_filter}
            GROUP BY customer_id
        )
        GROUP BY segment
    '''
    
    try:
        data = query_user_db(query)
        print(f"👥 Customer segments query returned: {len(data) if data else 0} rows")
        
        if not data:
            return jsonify({
                'labels': [],
                'values': []
            })
            
        total = sum(row['count'] for row in data)
        result = {
            'labels': [row['segment'] for row in data],
            'values': [round(row['count']/total*100, 1) for row in data]
        }
        print(f"👥 Segments result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in api_customer_segments: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-products')
@login_required
@database_required
def api_top_products():
    period = request.args.get('period', '60d')
    date_filter = get_date_filter(period)
    print(f"🏆 API Top Products called with period: {period}")
    
    query = f'''
        SELECT p.name, SUM(ti.quantity * ti.unit_price) as value
        FROM Transaction_Items ti
        JOIN Products p ON ti.product_id = p.id
        JOIN Transactions t ON ti.transaction_id = t.id
        WHERE date(t.timestamp) >= {date_filter}
        GROUP BY p.name
        ORDER BY value DESC
        LIMIT 10
    '''
    
    try:
        data = query_user_db(query)
        print(f"🏆 Top products query returned: {len(data) if data else 0} rows")
        result = [dict(row) for row in data] if data else []
        print(f"🏆 Top products: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in api_top_products: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/store-metrics')
@login_required
@database_required
def api_store_metrics():
    period = request.args.get('period', '60d')
    date_filter = get_date_filter(period)
    print(f"📈 API Store Metrics called with period: {period}")
    
    try:
        # Total sales
        sales_query = f'SELECT SUM(total_amount) FROM Transactions WHERE date(timestamp) >= {date_filter}'
        total_sales_result = query_user_db(sales_query, one=True)
        total_sales = total_sales_result[0] if total_sales_result and total_sales_result[0] is not None else 0
        
        # Transaction count
        trans_query = f'SELECT COUNT(*) FROM Transactions WHERE date(timestamp) >= {date_filter}'
        transaction_count_result = query_user_db(trans_query, one=True)
        transaction_count = transaction_count_result[0] if transaction_count_result and transaction_count_result[0] is not None else 0
        
        # Unique customers
        cust_query = f'SELECT COUNT(DISTINCT customer_id) FROM Transactions WHERE date(timestamp) >= {date_filter}'
        unique_customers_result = query_user_db(cust_query, one=True)
        unique_customers = unique_customers_result[0] if unique_customers_result and unique_customers_result[0] is not None else 0
        
        result = {
            'total_sales': round(total_sales, 2),
            'transaction_count': transaction_count,
            'unique_customers': unique_customers
        }
        print(f"📈 Store metrics: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in api_store_metrics: {e}")
        return jsonify({'error': str(e)}), 500

# PDF Download Routes
@app.route('/download-sales-report')
@login_required
@database_required
def download_sales_report():
    try:
        # Get current data
        period = request.args.get('period', '60d')
        sales_response = api_sales_data()
        sales_data = sales_response.get_json()
        
        # Calculate KPIs
        kpi_data = {
            'current_sales': sum(sales_data.get('actual', [])),
            'growth_rate': 0,  # Simplified - you can add proper calculation
            'avg_daily': sum(sales_data.get('actual', [])) / max(len(sales_data.get('actual', [])), 1),
            'period': period
        }
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = pdf_generator.generate_sales_report(
                session['current_store'], 
                sales_data, 
                kpi_data, 
                tmp_file.name
            )
            
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"sales_report_{session['current_store']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype='application/pdf'
            )
    except Exception as e:
        print(f"Error generating sales report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-customer-segments-report')
@login_required
@database_required
def download_customer_segments_report():
    try:
        # Get current data
        period = request.args.get('period', '60d')
        segments_response = api_customer_segments()
        segments_data = segments_response.get_json()
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = pdf_generator.generate_customer_segments_report(
                session['current_store'], 
                segments_data, 
                tmp_file.name
            )
            
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"customer_segments_{session['current_store']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype='application/pdf'
            )
    except Exception as e:
        print(f"Error generating customer segments report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-top-products-report')
@login_required
@database_required
def download_top_products_report():
    try:
        # Get current data
        period = request.args.get('period', '60d')
        products_response = api_top_products()
        products_data = products_response.get_json()
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = pdf_generator.generate_top_products_report(
                session['current_store'], 
                products_data, 
                tmp_file.name
            )
            
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"top_products_{session['current_store']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype='application/pdf'
            )
    except Exception as e:
        print(f"Error generating top products report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-store-performance-report')
@login_required
@database_required
def download_store_performance_report():
    try:
        # Get current data
        period = request.args.get('period', '60d')
        metrics_response = api_store_metrics()
        metrics_data = metrics_response.get_json()
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = pdf_generator.generate_store_performance_report(
                session['current_store'], 
                metrics_data, 
                tmp_file.name
            )
            
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"store_performance_{session['current_store']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype='application/pdf'
            )
    except Exception as e:
        print(f"Error generating store performance report: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)