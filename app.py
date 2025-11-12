#!/usr/bin/env python3
"""
GHMC Smart Waste Management System - Main Application
Author: Venkatesh Goulikar
Description: AI-powered waste management platform for Hyderabad GHMC
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ghmc-dev-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= ROUTES =============

@app.route('/')
def index():
    """Home page"""
    return jsonify({
        'service': 'GHMC Smart Waste Management API',
        'status': 'running',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/predict/bin-fill', methods=['POST'])
def predict_bin_fill():
    """
    Predict garbage bin fill level using ML model
    Expected JSON: {"bin_id": "BIN001", "location": "...", "historical_data": [...]}
    """
    try:
        data = request.json
        bin_id = data.get('bin_id')
        
        # Mock prediction (replace with actual ML model)
        prediction = {
            'bin_id': bin_id,
            'predicted_fill_level': 85,
            'collection_needed': True,
            'estimated_full_date': '2025-11-13',
            'confidence': 0.92
        }
        
        logger.info(f"Bin fill prediction for {bin_id}: {prediction['predicted_fill_level']}%")
        return jsonify(prediction), 200
        
    except Exception as e:
        logger.error(f"Error in bin fill prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize/route', methods=['POST'])
def optimize_route():
    """
    Optimize garbage collection route
    Expected JSON: {"bins": [{"id": "BIN001", "lat": 17.385, "lng": 78.486, "fill_level": 90}, ...]}
    """
    try:
        data = request.json
        bins = data.get('bins', [])
        
        # Mock route optimization (replace with actual algorithm)
        optimized_route = {
            'route': ['BIN001', 'BIN003', 'BIN005', 'BIN002', 'BIN004'],
            'total_distance_km': 12.5,
            'estimated_time_min': 45,
            'fuel_saved': '30%',
            'bins_to_collect': len(bins)
        }
        
        logger.info(f"Route optimized for {len(bins)} bins")
        return jsonify(optimized_route), 200
        
    except Exception as e:
        logger.error(f"Error in route optimization: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/complaints', methods=['GET', 'POST'])
def handle_complaints():
    """
    Handle citizen complaints
    """
    if request.method == 'POST':
        try:
            data = request.json
            complaint = {
                'id': 'COMP' + datetime.now().strftime('%Y%m%d%H%M%S'),
                'citizen_name': data.get('name'),
                'location': data.get('location'),
                'complaint': data.get('complaint'),
                'status': 'registered',
                'created_at': datetime.now().isoformat()
            }
            
            logger.info(f"New complaint registered: {complaint['id']}")
            return jsonify(complaint), 201
            
        except Exception as e:
            logger.error(f"Error registering complaint: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    # GET request - return mock complaints
    complaints = [
        {'id': 'COMP001', 'status': 'resolved', 'location': 'Kukatpally'},
        {'id': 'COMP002', 'status': 'in_progress', 'location': 'Ameerpet'}
    ]
    return jsonify(complaints), 200

@app.route('/api/stats')
def get_statistics():
    """
    Get system statistics
    """
    stats = {
        'total_bins': 1500,
        'bins_needing_collection': 125,
        'active_complaints': 23,
        'fuel_saved_percentage': 30,
        'citizen_satisfaction': 92,
        'collection_efficiency': 85
    }
    return jsonify(stats), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
