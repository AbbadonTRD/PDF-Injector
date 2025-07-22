#!/usr/bin/env python3
"""
IP Tracker - Flask-based geo-location logger with transparent pixel beacon
Author: GitHub Copilot
License: MIT
"""

import os
import io
import base64
import json
import logging
from datetime import datetime
from flask import Flask, Response, request, jsonify
import requests
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Thread-safe file writing
file_lock = Lock()

# Transparent 1x1 PNG in base64 (smallest possible PNG)
TRANSPARENT_PIXEL = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
)

def get_client_ip():
    """Extract real client IP considering proxies and load balancers"""
    # Check for forwarded headers (common in production environments)
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, take the first one
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def get_geo_data(ip_address):
    """Fetch geo-location data from ip-api.com"""
    try:
        # Use ip-api.com free tier - 1000 requests per hour
        url = f"http://ip-api.com/json/{ip_address}"
        
        # Add timeout to prevent hanging requests
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if API returned success
        if data.get('status') == 'success':
            return {
                'country': data.get('country', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'latitude': data.get('lat', 0.0),
                'longitude': data.get('lon', 0.0),
                'isp': data.get('isp', 'Unknown'),
                'timezone': data.get('timezone', 'Unknown'),
                'zip_code': data.get('zip', 'Unknown')
            }
        else:
            logger.warning(f"IP API returned error for {ip_address}: {data.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout when fetching geo data for IP: {ip_address}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error when fetching geo data for IP {ip_address}: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for IP {ip_address}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error when fetching geo data for IP {ip_address}: {str(e)}")
        return None

def log_request_data(ip_address, user_agent, geo_data):
    """Log request data to logs.txt file with thread safety"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare log entry
    log_entry = f"""
{'='*80}
TIMESTAMP: {timestamp}
IP ADDRESS: {ip_address}
USER AGENT: {user_agent}
"""
    
    if geo_data:
        log_entry += f"""LOCATION DATA:
  Country: {geo_data['country']}
  Region: {geo_data['region']}
  City: {geo_data['city']}
  Coordinates: {geo_data['latitude']}, {geo_data['longitude']}
  ISP: {geo_data['isp']}
  Timezone: {geo_data['timezone']}
  ZIP Code: {geo_data['zip_code']}
"""
    else:
        log_entry += "LOCATION DATA: Failed to retrieve geo-location data\n"
    
    log_entry += f"{'='*80}\n"
    
    # Thread-safe file writing
    with file_lock:
        try:
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(log_entry)
            logger.info(f"Successfully logged request from IP: {ip_address}")
        except Exception as e:
            logger.error(f"Failed to write to logs.txt: {str(e)}")

@app.route('/logger.png', methods=['GET'])
def pixel_logger():
    """Main endpoint that serves transparent pixel and logs request data"""
    try:
        # Get client information
        client_ip = get_client_ip()
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Console output for monitoring
        print(f"\n🎯 TRACKING REQUEST RECEIVED")
        print(f"   IP: {client_ip}")
        print(f"   User-Agent: {user_agent}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Fetch geo-location data
        geo_data = get_geo_data(client_ip)
        
        if geo_data:
            print(f"   Location: {geo_data['city']}, {geo_data['region']}, {geo_data['country']}")
            print(f"   ISP: {geo_data['isp']}")
        
        # Log the request data
        log_request_data(client_ip, user_agent, geo_data)
        
        # Return transparent 1x1 PNG
        return Response(
            io.BytesIO(TRANSPARENT_PIXEL).getvalue(),
            mimetype='image/png',
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0',
                'Content-Length': str(len(TRANSPARENT_PIXEL))
            }
        )
        
    except Exception as e:
        logger.error(f"Error in pixel_logger endpoint: {str(e)}")
        # Always return the pixel even if logging fails
        return Response(
            io.BytesIO(TRANSPARENT_PIXEL).getvalue(),
            mimetype='image/png'
        )

@app.route('/stats', methods=['GET'])
def get_stats():
    """Optional endpoint to view basic statistics"""
    try:
        if not os.path.exists('logs.txt'):
            return jsonify({'error': 'No logs available'})
        
        with open('logs.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Count number of requests
        request_count = content.count('TIMESTAMP:')
        
        return jsonify({
            'total_requests': request_count,
            'log_file_size': len(content),
            'status': 'active'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'IP Tracker',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

def initialize_log_file():
    """Initialize logs.txt file if it doesn't exist"""
    if not os.path.exists('logs.txt'):
        try:
            with open('logs.txt', 'w', encoding='utf-8') as f:
                f.write(f"IP TRACKER LOG FILE - CREATED ON {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n")
            logger.info("Created new logs.txt file")
        except Exception as e:
            logger.error(f"Failed to create logs.txt: {str(e)}")

if __name__ == '__main__':
    print("🚀 Starting IP Tracker Server...")
    print("📍 Geo-location API: ip-api.com")
    print("📝 Logs will be saved to: logs.txt")
    print("🔗 Pixel endpoint: http://0.0.0.0:5000/logger.png")
    print("📊 Stats endpoint: http://0.0.0.0:5000/stats")
    print("💚 Health check: http://0.0.0.0:5000/health")
    print("="*60)
    
    # Initialize log file
    initialize_log_file()
    
    # Start Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Set to False for production
        threaded=True  # Enable threading for concurrent requests
    )
