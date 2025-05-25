"""
Test script for TinyTroupe Service web interface
"""
import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app, db
from src.models import Conversation, Message, Persona, PersonaState

class TinyTroupeWebInterfaceTests(unittest.TestCase):
    """Test cases for TinyTroupe Service web interface"""
    
    def setUp(self):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Create test personas
            self.create_test_personas()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_test_personas(self):
        """Create test personas in the database"""
        with app.app_context():
            personas = [
                Persona(
                    id='warren_buffett',
                    name='Warren Buffett',
                    description='The most successful investor of modern times.',
                    personality={'traits': ['analytical', 'patient', 'disciplined']},
                    expertise=['value investing', 'business analysis', 'capital allocation']
                ),
                Persona(
                    id='albert_einstein',
                    name='Albert Einstein',
                    description='Renowned physicist with analytical thinking abilities.',
                    personality={'traits': ['curious', 'imaginative', 'analytical']},
                    expertise=['pattern recognition', 'systems thinking', 'thought experiments']
                )
            ]
            
            for persona in personas:
                db.session.add(persona)
            
            db.session.commit()
    
    def test_home_page(self):
        """Test that the home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TinyTroupe Financial Advisors', response.data)
    
    def test_create_conversation(self):
        """Test creating a new conversation"""
        response = self.client.post(
            '/api/conversations',
            json={
                'title': 'Test Conversation',
                'user_id': 'test_user'
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Conversation')
        self.assertEqual(data['user_id'], 'test_user')
        
        # Verify conversation was created in database
        with app.app_context():
            conversation = Conversation.query.get(data['id'])
            self.assertIsNotNone(conversation)
            self.assertEqual(conversation.title, 'Test Conversation')
            
            # Verify persona states were created
            persona_states = PersonaState.query.filter_by(conversation_id=data['id']).all()
            self.assertEqual(len(persona_states), 2)  # Two test personas
    
    def test_get_conversations(self):
        """Test retrieving conversations"""
        # Create a test conversation
        self.client.post(
            '/api/conversations',
            json={
                'title': 'Test Conversation',
                'user_id': 'test_user'
            }
        )
        
        # Get conversations
        response = self.client.get('/api/conversations?user_id=test_user')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Conversation')
    
    @patch('src.services.tinytroupe_service.TinyTroupeService.get_response')
    def test_send_message(self, mock_get_response):
        """Test sending a message and getting advisor responses"""
        # Mock the TinyTroupe service response
        mock_get_response.return_value = "This is a test response from the advisor."
        
        # Create a test conversation
        conversation_response = self.client.post(
            '/api/conversations',
            json={
                'title': 'Test Conversation',
                'user_id': 'test_user'
            }
        )
        conversation_data = json.loads(conversation_response.data)
        conversation_id = conversation_data['id']
        
        # Send a message
        message_response = self.client.post(
            f'/api/conversations/{conversation_id}/messages',
            json={
                'content': 'This is a test message.'
            }
        )
        
        self.assertEqual(message_response.status_code, 201)
        message_data = json.loads(message_response.data)
        
        # Verify user message
        self.assertEqual(message_data['user_message']['content'], 'This is a test message.')
        
        # Verify advisor responses
        self.assertEqual(len(message_data['advisor_responses']), 2)  # Two test personas
        for response in message_data['advisor_responses']:
            self.assertEqual(response['content'], "This is a test response from the advisor.")
        
        # Verify messages were created in database
        with app.app_context():
            messages = Message.query.filter_by(conversation_id=conversation_id).all()
            self.assertEqual(len(messages), 3)  # 1 user message + 2 advisor responses
    
    @patch('src.services.financial_service.FinancialService.get_stock_data')
    @patch('src.services.tinytroupe_service.TinyTroupeService.analyze_stock')
    def test_stock_analysis(self, mock_analyze_stock, mock_get_stock_data):
        """Test stock analysis endpoint"""
        # Mock the financial service responses
        mock_get_stock_data.return_value = {
            "symbol": "AAPL",
            "price": 150.0,
            "change": 2.5,
            "change_percent": 1.7,
            "market_cap": "2.5T",
            "pe_ratio": 28.5,
            "dividend_yield": 0.6,
            "52_week_high": 180.0,
            "52_week_low": 120.0,
            "data_source": "Test Data"
        }
        
        mock_analyze_stock.return_value = {
            "warren_buffett": {
                "name": "Warren Buffett",
                "summary": "Test summary from Warren Buffett",
                "recommendation": "Test recommendation from Warren Buffett"
            },
            "albert_einstein": {
                "name": "Albert Einstein",
                "summary": "Test summary from Albert Einstein",
                "recommendation": "Test recommendation from Albert Einstein"
            }
        }
        
        # Get stock analysis
        response = self.client.get('/api/financial-data/AAPL/analysis')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify stock data
        self.assertEqual(data['stock_data']['symbol'], 'AAPL')
        self.assertEqual(data['stock_data']['price'], 150.0)
        
        # Verify advisor analysis
        self.assertEqual(len(data['advisor_analysis']), 2)
        self.assertEqual(data['advisor_analysis']['warren_buffett']['name'], 'Warren Buffett')
        self.assertEqual(data['advisor_analysis']['albert_einstein']['name'], 'Albert Einstein')

if __name__ == '__main__':
    unittest.main()
