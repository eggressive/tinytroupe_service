"""
Test script for TinyTroupe Service CLI interface
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.tinytroupe_cli import TinyTroupeCLI

class TinyTroupeCLITests(unittest.TestCase):
    """Test cases for TinyTroupe Service CLI interface"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for config files
        self.test_dir = tempfile.mkdtemp()
        
        # Initialize CLI with test directory
        self.cli = TinyTroupeCLI(server_url="http://localhost:5000")
        self.cli.config_dir = self.test_dir
        self.cli.config_file = os.path.join(self.test_dir, "config.json")
        self.cli.history_file = os.path.join(self.test_dir, "history.json")
        
        # Save default config
        self.cli._save_config()
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    @patch('requests.get')
    def test_list_conversations(self, mock_get):
        """Test listing conversations"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                'id': '12345678-1234-5678-1234-567812345678',
                'title': 'Test Conversation',
                'created_at': '2025-05-25T15:00:00',
                'updated_at': '2025-05-25T15:10:00',
                'message_count': 5
            }
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        conversations = self.cli.list_conversations()
        
        # Verify API was called correctly
        mock_get.assert_called_once_with(
            "http://localhost:5000/api/conversations",
            params={"user_id": "default_user"}
        )
        
        # Verify result
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['title'], 'Test Conversation')
    
    @patch('requests.post')
    def test_create_conversation(self, mock_post):
        """Test creating a conversation"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': '12345678-1234-5678-1234-567812345678',
            'title': 'Test Conversation',
            'user_id': 'default_user',
            'created_at': '2025-05-25T15:00:00',
            'updated_at': '2025-05-25T15:00:00'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call method
        conversation = self.cli.create_conversation("Test Conversation")
        
        # Verify API was called correctly
        mock_post.assert_called_once_with(
            "http://localhost:5000/api/conversations",
            json={
                "user_id": "default_user",
                "title": "Test Conversation"
            }
        )
        
        # Verify result
        self.assertEqual(conversation['title'], 'Test Conversation')
        
        # Verify conversation was added to history
        history = self.cli._load_history()
        self.assertEqual(len(history['conversations']), 1)
        self.assertEqual(history['conversations'][0]['title'], 'Test Conversation')
    
    @patch('requests.get')
    def test_get_messages(self, mock_get):
        """Test getting messages"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                'id': '12345678-1234-5678-1234-567812345678',
                'conversation_id': '87654321-8765-4321-8765-432187654321',
                'role': 'user',
                'content': 'Test message',
                'timestamp': '2025-05-25T15:00:00'
            },
            {
                'id': '23456789-2345-6789-2345-678923456789',
                'conversation_id': '87654321-8765-4321-8765-432187654321',
                'role': 'advisor',
                'advisor_id': 'warren_buffett',
                'content': 'Test response',
                'timestamp': '2025-05-25T15:00:05'
            }
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        messages = self.cli.get_messages("87654321-8765-4321-8765-432187654321")
        
        # Verify API was called correctly
        mock_get.assert_called_once_with(
            "http://localhost:5000/api/conversations/87654321-8765-4321-8765-432187654321/messages"
        )
        
        # Verify result
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'user')
        self.assertEqual(messages[0]['content'], 'Test message')
        self.assertEqual(messages[1]['role'], 'advisor')
        self.assertEqual(messages[1]['content'], 'Test response')
    
    @patch('requests.post')
    def test_send_message(self, mock_post):
        """Test sending a message"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'user_message': {
                'id': '12345678-1234-5678-1234-567812345678',
                'conversation_id': '87654321-8765-4321-8765-432187654321',
                'role': 'user',
                'content': 'Test message',
                'timestamp': '2025-05-25T15:00:00'
            },
            'advisor_responses': [
                {
                    'id': '23456789-2345-6789-2345-678923456789',
                    'advisor_id': 'warren_buffett',
                    'advisor_name': 'Warren Buffett',
                    'content': 'Test response from Warren Buffett',
                    'timestamp': '2025-05-25T15:00:05'
                },
                {
                    'id': '34567890-3456-7890-3456-789034567890',
                    'advisor_id': 'albert_einstein',
                    'advisor_name': 'Albert Einstein',
                    'content': 'Test response from Albert Einstein',
                    'timestamp': '2025-05-25T15:00:05'
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Call method
        result = self.cli.send_message("87654321-8765-4321-8765-432187654321", "Test message")
        
        # Verify API was called correctly
        mock_post.assert_called_once_with(
            "http://localhost:5000/api/conversations/87654321-8765-4321-8765-432187654321/messages",
            json={"content": "Test message"}
        )
        
        # Verify result
        self.assertEqual(result['user_message']['content'], 'Test message')
        self.assertEqual(len(result['advisor_responses']), 2)
        self.assertEqual(result['advisor_responses'][0]['advisor_name'], 'Warren Buffett')
        self.assertEqual(result['advisor_responses'][1]['advisor_name'], 'Albert Einstein')
    
    @patch('requests.get')
    def test_analyze_stock(self, mock_get):
        """Test analyzing a stock"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'stock_data': {
                'symbol': 'AAPL',
                'price': 150.0,
                'change': 2.5,
                'change_percent': 1.7,
                'market_cap': '2.5T',
                'pe_ratio': 28.5,
                'dividend_yield': 0.6,
                '52_week_high': 180.0,
                '52_week_low': 120.0,
                'data_source': 'Test Data'
            },
            'advisor_analysis': {
                'warren_buffett': {
                    'name': 'Warren Buffett',
                    'summary': 'Test summary from Warren Buffett',
                    'recommendation': 'Test recommendation from Warren Buffett'
                },
                'albert_einstein': {
                    'name': 'Albert Einstein',
                    'summary': 'Test summary from Albert Einstein',
                    'recommendation': 'Test recommendation from Albert Einstein'
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call method
        analysis = self.cli.analyze_stock("AAPL")
        
        # Verify API was called correctly
        mock_get.assert_called_once_with(
            "http://localhost:5000/api/financial-data/AAPL/analysis"
        )
        
        # Verify result
        self.assertEqual(analysis['stock_data']['symbol'], 'AAPL')
        self.assertEqual(analysis['stock_data']['price'], 150.0)
        self.assertEqual(len(analysis['advisor_analysis']), 2)
        
        # Verify analysis was added to history
        history = self.cli._load_history()
        self.assertEqual(len(history['analyses']), 1)
        self.assertEqual(history['analyses'][0]['symbol'], 'AAPL')
    
    def test_configure(self):
        """Test configuring the CLI"""
        # Call method
        self.cli.configure(server_url="http://example.com", user_id="test_user")
        
        # Verify config was updated
        config = self.cli._load_config()
        self.assertEqual(config['server_url'], 'http://example.com')
        self.assertEqual(config['user_id'], 'test_user')

if __name__ == '__main__':
    unittest.main()
