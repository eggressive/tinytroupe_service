# TinyTroupe Financial Advisors - User Guide

## Overview

TinyTroupe Financial Advisors is a personal service that leverages Microsoft's TinyTroupe library to simulate a team of financial experts who can provide investment advice and analysis. The service offers both web-based and command-line interfaces, supports ongoing dialogues with persistent memory, and can integrate with financial data sources.

This guide will help you set up, run, and maintain the service on your local machine, with instructions for future deployment to Docker containers or cloud environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Project Architecture](#project-architecture)
5. [Setting Up Financial API Keys](#setting-up-financial-api-keys)
6. [Running the Service](#running-the-service)
7. [Using the Web Interface](#using-the-web-interface)
8. [Using the CLI](#using-the-cli)
9. [Maintenance](#maintenance)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Deployment](#advanced-deployment)
12. [Security Considerations](#security-considerations)

## System Requirements

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API key or Azure OpenAI API key
- Internet connection for financial data retrieval

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/tinytroupe_service.git
cd tinytroupe_service
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install TinyTroupe Library

The TinyTroupe library needs to be installed directly from Microsoft's GitHub repository:

```bash
pip install git+https://github.com/microsoft/TinyTroupe.git
```

## Configuration

### Configuration Step 1: Create Environment Variables File

Create a `.env` file in the root directory with the following variables:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key
# OR for Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=2023-05-15

# Database Configuration
DATABASE_URI=sqlite:///tinytroupe.db

# Financial API Keys (Optional)
YAHOO_FINANCE_API_KEY=your_yahoo_finance_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

# Application Configuration
SECRET_KEY=your_secret_key
FLASK_DEBUG=False
```

For SECRET_KEY, you can generate a random string or use a secure password manager.
e.g. ```python -c "import secrets; print(secrets.token_hex(16))"```

## Project Architecture

TinyTroupe Financial Advisors follows a modular architecture to ensure maintainability and prevent circular dependencies:

### Directory Structure

```bash
tinytroupe_service/
├── backup/                # Backup directory
├── cli/                   # Command-line interface
│   └── commands/          # CLI command implementations
├── instance/              # SQLite database location
├── src/                   # Main application code
│   ├── extensions.py      # Shared Flask extensions
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration management
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── static/            # Static assets
│   │   ├── css/           # Stylesheets
│   │   ├── images/        # Image assets
│   │   └── js/            # JavaScript files
│   └── templates/         # HTML templates
└── tests/                 # Test files and scripts
    ├── debug_env.py       # Environment debugging script
    ├── final_test.py      # Final verification script
    ├── test_service.py    # Service testing script
    └── test_*.py          # Additional test files
```

### Key Components

1. **Extensions Module**: Centralizes Flask extensions like SQLAlchemy and CORS to avoid circular imports:

   ```python
   # src/extensions.py
   from flask_sqlalchemy import SQLAlchemy
   from flask_cors import CORS

   db = SQLAlchemy()  # Used in models and services
   cors = CORS()      # Used for Cross-Origin Resource Sharing
   ```

2. **Main Application**: Initializes and configures the Flask app:

   ```python
   # src/main.py
   from src.extensions import db, cors
   
   app = Flask(__name__)
   # Configure app...
   
   # Initialize extensions with app
   db.init_app(app)
   cors.init_app(app)
   ```

3. **Models**: Database schemas using SQLAlchemy with proper imports:

   ```python
   # src/models/some_model.py
   from src.extensions import db  # Import db from extensions, not main
   
   class SomeModel(db.Model):
       # Model definition...
   ```

This architecture prevents common circular import issues in Flask applications and improves maintainability.

## Setting Up Financial API Keys

### Yahoo Finance API Key Setup

Yahoo Finance doesn't offer a direct API service. Instead, you'll need to use RapidAPI to access Yahoo Finance data:

1. **Sign up for RapidAPI**:
   - Go to [https://rapidapi.com/](https://rapidapi.com/)
   - Click "Sign Up" and create an account

2. **Subscribe to Yahoo Finance API**:
   - Search for "Yahoo Finance" in the RapidAPI marketplace
   - Select one of the Yahoo Finance API providers (popular ones include Yahoo Finance by API Dojo or Yahoo Finance by apibridge)
   - Review the pricing plans (they typically offer a free tier with limited requests)
   - Click "Subscribe to Test" for your chosen plan

3. **Get your API Key**:
   - After subscribing, you'll be provided with an API key (also called "X-RapidAPI-Key")
   - This key will be visible in the "Header Parameters" section of any endpoint documentation
   - Copy this key for use in your TinyTroupe service

4. **Add the API Key to your environment**:
   - Add the API key to your `.env` file:

     ```bash
     YAHOO_FINANCE_API_KEY=your_rapidapi_key_here
     ```

5. **Update the FinancialService class** (if needed):
   - Open `src/services/financial_service.py`
   - Update the `__init__` method to include RapidAPI headers:

     ```python
     def __init__(self):
         """Initialize the financial service"""
         self.logger = logging.getLogger(__name__)
         self.yahoo_finance_api_key = os.getenv('YAHOO_FINANCE_API_KEY')
         self.alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
         
         # Add RapidAPI headers for Yahoo Finance
         self.yahoo_finance_headers = {
             'X-RapidAPI-Key': self.yahoo_finance_api_key,
             'X-RapidAPI-Host': 'yahoo-finance15.p.rapidapi.com'  # This may vary based on your provider
         }
     ```

   - Update API request methods to use these headers:

     ```python
     def get_stock_data(self, symbol):
         """Get stock data from Yahoo Finance"""
         try:
             url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}"
             response = requests.get(url, headers=self.yahoo_finance_headers)
             response.raise_for_status()
             # Process response...
         except Exception as e:
             self.logger.error(f"Error fetching stock data: {str(e)}")
             # Handle error...
     ```

Note: RapidAPI's free tiers typically have daily request limits. For a production environment, you might want to consider a paid plan based on your usage requirements.

### Alpha Vantage API Key Setup (Alternative)

Alpha Vantage is another popular financial data provider:

1. Go to [https://www.alphavantage.co/](https://www.alphavantage.co/)
2. Sign up for a free API key
3. Add the key to your `.env` file:

   ```bash
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   ```

### Configuration Step 2: Initialize the Database

```bash
python -c "from src.extensions import db; from src.main import app; app.app_context().push(); db.create_all()"
```

## Running the Service

### Starting the Web Server

```bash
python src/main.py
```

By default, the server will run on `http://localhost:5000`. You can access the web interface by opening this URL in your browser.

### CLI Setup

The CLI tool can be used alongside the web interface. First, make the CLI script executable:

```bash
chmod +x cli/tinytroupe_cli.py
```

Then, you can create a symbolic link to make it available system-wide (optional):

```bash
sudo ln -s $(pwd)/cli/tinytroupe_cli.py /usr/local/bin/tinytroupe
```

## Using the Web Interface

The web interface provides an intuitive way to interact with your financial advisors.

### Home Page

The home page allows you to:

- Start new conversations
- Access recent conversations
- View your advisory team

### Conversation Page

In a conversation, you can:

- Send messages to your advisors
- View responses from each advisor
- See the conversation history

### Stock Analysis Page

The stock analysis page allows you to:

- Analyze specific stocks by symbol
- View financial data and metrics
- Get personalized analysis from each advisor

## Using the CLI

The CLI provides command-line access to the same functionality as the web interface.

### Available Commands

```bash
tinytroupe --help                        # Show help
tinytroupe list                          # List all conversations
tinytroupe start --title "My Analysis"   # Start a new conversation
tinytroupe continue <conversation_id>    # Continue an existing conversation
tinytroupe analyze AAPL                  # Analyze a stock symbol
tinytroupe config --server http://localhost:5000 --user default_user  # Configure CLI
```

### Examples

Starting a new conversation:

```bash
tinytroupe start --title "Portfolio Review"
```

Analyzing a stock:

```bash
tinytroupe analyze AAPL
```

## Maintenance

### Backing Up the Database

The SQLite database file is located at `tinytroupe.db` in the root directory. To back it up:

```bash
cp tinytroupe.db tinytroupe_backup_$(date +%Y%m%d).db
```

### Updating Dependencies

To update all dependencies to their latest compatible versions:

```bash
pip install --upgrade -r requirements.txt
```

### Updating TinyTroupe Library

To update the TinyTroupe library to the latest version:

```bash
pip install --upgrade git+https://github.com/microsoft/TinyTroupe.git
```

## Testing and Verification

The project includes several test scripts in the `tests/` directory to help verify that everything is working correctly:

### Complete System Verification

To run a comprehensive test of all components:

```bash
cd /path/to/tinytroupe_service
source venv/bin/activate  # Activate virtual environment
python tests/verification.py
```

This script will test:

- Environment variable loading from `.env` file
- Config class initialization
- TinyTroupe service API key access
- Flask application availability (if running)

### Environment Variable Testing

To verify that environment variables are loading correctly:

```bash
cd /path/to/tinytroupe_service
python tests/debug_env.py
```

This script will show:

- Whether environment variables are loaded before and after `load_dotenv()`
- The current working directory and file paths
- Whether the Config class is reading variables correctly

### TinyTroupe Service Testing

To test that the TinyTroupe service can access the API key:

```bash
cd /path/to/tinytroupe_service
source venv/bin/activate  # Activate virtual environment
python tests/final_test.py
```

### Web Interface Testing

You can run the web interface tests using pytest:

```bash
cd /path/to/tinytroupe_service
source venv/bin/activate
python -m pytest tests/test_web_interface.py -v
```

### CLI Interface Testing

To test the CLI interface:

```bash
cd /path/to/tinytroupe_service
source venv/bin/activate
python -m pytest tests/test_cli_interface.py -v
```

### Quick API Verification

To quickly verify that the API is working:

```bash
# Start the Flask application
source venv/bin/activate
python -m src.main &

# Test creating a conversation
curl -s http://localhost:5000/api/conversations -X POST \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Conversation"}'

# Test adding a message (replace CONVERSATION_ID with actual ID from above)
curl -s http://localhost:5000/api/conversations/CONVERSATION_ID/messages -X POST \
  -H "Content-Type: application/json" \
  -d '{"content":"What are your thoughts on value investing?"}'
```

## Troubleshooting

### Common Issues

#### API Key Issues

If you see errors related to API keys:

1. Verify that your `.env` file contains the correct API keys
2. Ensure the environment variables are being loaded properly
3. Check that you have sufficient credits/quota on your OpenAI account
4. For Yahoo Finance API via RapidAPI, verify that:
   - Your subscription is active
   - You're using the correct RapidAPI host in your headers
   - You haven't exceeded your daily request limit

**Common API Key Loading Issues:**

- **Error**: "No OpenAI or Azure OpenAI API key found. TinyTroupe will not function properly."
  - **Solution**: Ensure your `.env` file is in the project root directory (same level as `src/` folder)
  - **Verification**: Test with: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"`

- **Error**: Environment variables not loading from `.env` file
  - **Cause**: Invalid comment syntax in `.env` file
  - **Solution**: Use `#` for comments in `.env` files, not `//` or other comment styles

#### Database Issues

If you encounter database errors:

1. Ensure the database file exists and is writable
2. Try reinitializing the database using the command in the Configuration section
3. Check for disk space issues

#### Connection Issues

If the CLI cannot connect to the server:

1. Verify the server is running
2. Check the server URL in the CLI configuration
3. Ensure there are no firewall issues blocking the connection

#### Import Errors

If you encounter circular import errors:

1. Check that you're importing `db` from `src.extensions` and not from `src.main`
2. Ensure your project follows the architecture pattern described in [Project Architecture](#project-architecture)
3. Move imports inside functions if you need to break circular dependencies in complex cases

## Advanced Deployment

### Docker Deployment

A Dockerfile is provided for containerizing the application:

```bash
# Build the Docker image
docker build -t tinytroupe-service .

# Run the container
docker run -p 5000:5000 --env-file .env tinytroupe-service
```

### Docker Compose

For a more complete setup with proper volume mounting:

```bash
docker-compose up -d
```

### EC2 Deployment

To deploy on an AWS EC2 instance:

1. Launch an EC2 instance with Ubuntu
2. Install Docker on the instance
3. Clone the repository and build the Docker image
4. Set up a systemd service to ensure the container runs on startup
5. Configure Nginx as a reverse proxy for HTTPS support

Example systemd service file (`/etc/systemd/system/tinytroupe.service`):

```ini
[Unit]
Description=TinyTroupe Financial Advisors
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
ExecStartPre=-/usr/bin/docker stop tinytroupe
ExecStartPre=-/usr/bin/docker rm tinytroupe
ExecStart=/usr/bin/docker run --name tinytroupe -p 5000:5000 --env-file /path/to/.env tinytroupe-service

[Install]
WantedBy=multi-user.target
```

## Security Considerations

### Authentication

The initial implementation is for personal use without authentication. To add basic authentication:

1. Install Flask-Login:

   ```bash
   pip install flask-login
   ```

2. Implement user authentication in the Flask application
3. Update the CLI to support authentication

### API Key Management

Always keep your API keys secure:

- Never commit `.env` files to version control
- Use environment variables for production deployments
- Consider using a secrets manager for cloud deployments

### HTTPS

For production deployments, always use HTTPS:

- Set up a reverse proxy like Nginx with Let's Encrypt
- Configure proper SSL/TLS settings
- Redirect all HTTP traffic to HTTPS

## Next Steps

As you continue using and developing the TinyTroupe Financial Advisors service, consider:

1. Enhancing the advisor personas with more specialized expertise
2. Integrating additional financial data sources
3. Implementing more sophisticated analysis techniques
4. Adding visualization capabilities for financial data
5. Developing a mobile app interface

For any questions or issues, please refer to the documentation or contact support.
