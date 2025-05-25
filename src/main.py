"""
Main Flask application entry point for TinyTroupe Service
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # Required for Flask deployment

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///tinytroupe.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')

# Initialize database
db = SQLAlchemy(app)

# Import routes after app initialization to avoid circular imports
from src.routes.conversation import conversation_bp
from src.routes.advisor import advisor_bp
from src.routes.financial import financial_bp

# Register blueprints
app.register_blueprint(conversation_bp, url_prefix='/api/conversations')
app.register_blueprint(advisor_bp, url_prefix='/api/advisors')
app.register_blueprint(financial_bp, url_prefix='/api/financial-data')

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/conversation/<conversation_id>')
def conversation(conversation_id):
    """Render the conversation page"""
    return render_template('conversation.html', conversation_id=conversation_id)

@app.route('/analysis')
def analysis():
    """Render the financial analysis page"""
    return render_template('analysis.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
