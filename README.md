# Project Documentation

## Overview
This project is a web application built using Flask that provides analytics and reporting features for retail stores. Users can upload their SQLite databases, view sales trends, customer segments, top products, and store performance metrics. The application also generates PDF reports for various analytics.

## Project Structure
```
project
├── app.py                     # Main application logic using Flask
├── requirements.txt           # Python dependencies required for the application
├── config.py                  # Configuration settings for the application
├── utils                      # Utility functions and modules
│   ├── __init__.py           # Marks the utils directory as a package
│   ├── analytics.py           # Functions for data analysis
│   ├── database_utils.py      # Utility functions for database interactions
│   ├── helpers.py             # Helper functions used throughout the application
│   └── pdf_generator.py       # Functionality for generating PDF reports
├── templates                  # HTML templates for the application
│   ├── login.html             # Template for the login page
│   ├── store_selection.html    # Template for selecting a store
│   ├── upload_database.html    # Template for uploading a database
│   ├── sales_trends.html       # Template for displaying sales trends
│   ├── customer_segments.html   # Template for displaying customer segments
│   ├── top_products.html       # Template for displaying top products
│   ├── store_performance.html   # Template for displaying store performance
│   └── dashboard.html          # Template for the dashboard
├── README.md                  # Documentation for the project
└── render.yaml                # Configuration for deploying the application on Render.com
```

## Requirements
The application requires the following Python packages:
- Flask
- SQLite
- NumPy
- Pandas

These dependencies are listed in the `requirements.txt` file.

## Deployment
To host the application on Render.com, the `render.yaml` file is configured as follows:

```yaml
version: 1
services:
  - type: web
    name: your-app-name
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    autoDeploy: true
```

Make sure to replace `your-app-name` with the desired name for your application.

## Usage
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
4. Access the application in your web browser at `http://localhost:5000`.

## License
This project is licensed under the MIT License.