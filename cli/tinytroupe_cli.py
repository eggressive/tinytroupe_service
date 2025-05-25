#!/usr/bin/env python3
"""
TinyTroupe CLI - Command-line interface for TinyTroupe Financial Advisors
"""
import os
import sys
import json
import click
import requests
from tabulate import tabulate
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Default server URL
DEFAULT_SERVER = "http://localhost:5000"

class TinyTroupeCLI:
    """CLI client for TinyTroupe service"""
    
    def __init__(self, server_url=None):
        """Initialize the CLI client"""
        self.server_url = server_url or os.getenv('TINYTROUPE_SERVER', DEFAULT_SERVER)
        self.config_dir = os.path.expanduser("~/.tinytroupe")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.history_file = os.path.join(self.config_dir, "history.json")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load config
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "server_url": self.server_url,
            "user_id": "default_user"
        }
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_history(self):
        """Load conversation history from file"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {"conversations": [], "analyses": []}
    
    def _save_history(self, history):
        """Save conversation history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _add_to_history(self, history_type, item):
        """Add an item to history"""
        history = self._load_history()
        
        # Add item to appropriate history list
        if history_type not in history:
            history[history_type] = []
        
        # Check if item already exists
        for i, existing in enumerate(history[history_type]):
            if existing.get('id') == item.get('id'):
                # Update existing item
                history[history_type][i] = item
                self._save_history(history)
                return
        
        # Add new item
        history[history_type].append(item)
        
        # Limit to 10 items
        if len(history[history_type]) > 10:
            history[history_type] = history[history_type][-10:]
        
        self._save_history(history)
    
    def list_conversations(self):
        """List all conversations"""
        try:
            response = requests.get(
                f"{self.config['server_url']}/api/conversations",
                params={"user_id": self.config["user_id"]}
            )
            response.raise_for_status()
            conversations = response.json()
            
            if not conversations:
                click.echo("No conversations found.")
                return []
            
            # Format as table
            table_data = []
            for conv in conversations:
                created_at = datetime.fromisoformat(conv['created_at'].replace('Z', '+00:00'))
                table_data.append([
                    conv['id'][:8] + '...',
                    conv['title'],
                    created_at.strftime('%Y-%m-%d %H:%M'),
                    conv.get('message_count', 0)
                ])
            
            click.echo(tabulate(
                table_data,
                headers=["ID", "Title", "Created", "Messages"],
                tablefmt="pretty"
            ))
            
            return conversations
            
        except requests.RequestException as e:
            click.echo(f"Error: Could not retrieve conversations. {str(e)}")
            return []
    
    def create_conversation(self, title):
        """Create a new conversation"""
        try:
            response = requests.post(
                f"{self.config['server_url']}/api/conversations",
                json={
                    "user_id": self.config["user_id"],
                    "title": title
                }
            )
            response.raise_for_status()
            conversation = response.json()
            
            click.echo(f"Created conversation: {conversation['title']} (ID: {conversation['id']})")
            
            # Add to history
            self._add_to_history("conversations", conversation)
            
            return conversation
            
        except requests.RequestException as e:
            click.echo(f"Error: Could not create conversation. {str(e)}")
            return None
    
    def get_messages(self, conversation_id):
        """Get messages for a conversation"""
        try:
            response = requests.get(
                f"{self.config['server_url']}/api/conversations/{conversation_id}/messages"
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            click.echo(f"Error: Could not retrieve messages. {str(e)}")
            return []
    
    def send_message(self, conversation_id, content):
        """Send a message in a conversation"""
        try:
            response = requests.post(
                f"{self.config['server_url']}/api/conversations/{conversation_id}/messages",
                json={"content": content}
            )
            response.raise_for_status()
            result = response.json()
            
            # Display user message
            user_message = result['user_message']
            click.echo(f"\nYou: {user_message['content']}")
            
            # Display advisor responses
            for resp in result['advisor_responses']:
                advisor_name = resp['advisor_name']
                click.echo(f"\n{advisor_name}:\n{resp['content']}")
            
            return result
            
        except requests.RequestException as e:
            click.echo(f"Error: Could not send message. {str(e)}")
            return None
    
    def analyze_stock(self, symbol):
        """Analyze a stock"""
        try:
            click.echo(f"Analyzing {symbol}...")
            response = requests.get(
                f"{self.config['server_url']}/api/financial-data/{symbol}/analysis"
            )
            response.raise_for_status()
            analysis = response.json()
            
            # Display stock data
            stock_data = analysis['stock_data']
            click.echo("\nStock Data:")
            click.echo(f"Symbol: {symbol}")
            click.echo(f"Price: ${stock_data['price']:.2f}")
            click.echo(f"Change: {stock_data['change']:.2f} ({stock_data['change_percent']:.2f}%)")
            click.echo(f"Market Cap: {stock_data['market_cap']}")
            click.echo(f"P/E Ratio: {stock_data['pe_ratio']:.2f}")
            click.echo(f"Dividend Yield: {stock_data['dividend_yield']:.2f}%")
            click.echo(f"52-Week Range: ${stock_data['52_week_low']:.2f} - ${stock_data['52_week_high']:.2f}")
            click.echo(f"Source: {stock_data['data_source']}")
            
            # Display advisor analysis
            click.echo("\nAdvisor Analysis:")
            for advisor_id, advisor_analysis in analysis['advisor_analysis'].items():
                click.echo(f"\n{advisor_analysis['name']}:")
                click.echo(f"Summary: {advisor_analysis['summary']}")
                click.echo(f"Recommendation: {advisor_analysis['recommendation']}")
            
            # Add to history
            self._add_to_history("analyses", {
                "id": symbol,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "price": stock_data['price']
            })
            
            return analysis
            
        except requests.RequestException as e:
            click.echo(f"Error: Could not analyze stock. {str(e)}")
            return None
    
    def configure(self, server_url=None, user_id=None):
        """Configure the CLI client"""
        if server_url:
            self.config['server_url'] = server_url
        
        if user_id:
            self.config['user_id'] = user_id
        
        self._save_config()
        click.echo("Configuration saved.")
        click.echo(f"Server URL: {self.config['server_url']}")
        click.echo(f"User ID: {self.config['user_id']}")


@click.group()
@click.option('--server', help='TinyTroupe server URL')
@click.pass_context
def cli(ctx, server):
    """TinyTroupe Financial Advisors CLI"""
    ctx.obj = TinyTroupeCLI(server_url=server)


@cli.command('list')
@click.pass_obj
def list_conversations(cli_client):
    """List all conversations"""
    cli_client.list_conversations()


@cli.command('start')
@click.option('--title', '-t', default="New Conversation", help='Conversation title')
@click.pass_obj
def start_conversation(cli_client, title):
    """Start a new conversation"""
    conversation = cli_client.create_conversation(title)
    if conversation:
        click.echo("Type your message and press Enter to send. Type 'exit' to quit.")
        while True:
            content = click.prompt("You", type=str)
            if content.lower() == 'exit':
                break
            cli_client.send_message(conversation['id'], content)


@cli.command('continue')
@click.argument('conversation_id')
@click.pass_obj
def continue_conversation(cli_client, conversation_id):
    """Continue an existing conversation"""
    # Get messages
    messages = cli_client.get_messages(conversation_id)
    
    if messages:
        click.echo("Previous messages:")
        for msg in messages:
            if msg['role'] == 'user':
                click.echo(f"You: {msg['content']}")
            else:
                advisor_id = msg['advisor_id'] or 'Unknown'
                click.echo(f"{advisor_id}: {msg['content']}")
    
    click.echo("\nType your message and press Enter to send. Type 'exit' to quit.")
    while True:
        content = click.prompt("You", type=str)
        if content.lower() == 'exit':
            break
        cli_client.send_message(conversation_id, content)


@cli.command('analyze')
@click.argument('symbol')
@click.pass_obj
def analyze_stock(cli_client, symbol):
    """Analyze a stock symbol"""
    cli_client.analyze_stock(symbol.upper())


@cli.command('config')
@click.option('--server', help='TinyTroupe server URL')
@click.option('--user', help='User ID')
@click.pass_obj
def configure(cli_client, server, user):
    """Configure the CLI client"""
    cli_client.configure(server_url=server, user_id=user)


if __name__ == '__main__':
    cli()
