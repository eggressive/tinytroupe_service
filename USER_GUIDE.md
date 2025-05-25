# TinyTroupe Financial Advisors - User Guide

## Overview

TinyTroupe Financial Advisors is a personal service that leverages Microsoft's TinyTroupe library to simulate a team of financial experts who can provide investment advice and analysis. The service offers both web-based and command-line interfaces, supports ongoing dialogues with persistent memory, and can integrate with financial data sources.

This guide will help you set up, run, and maintain the service on your local machine, with instructions for future deployment to Docker containers or cloud environments.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Service](#running-the-service)
5. [Using the Web Interface](#using-the-web-interface)
6. [Using the CLI](#using-the-cli)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Deployment](#advanced-deployment)
10. [Security Considerations](#security-considerations)

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

### Step 1: Create Environment Variables File

Create a `.env` file in the root directory with the following variables:

```
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

### Step 2: Initialize the Database

```bash
python -c "from src.main import app, db; app.app_context().push(); db.create_all()"
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

```
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

## Troubleshooting

### Common Issues

#### API Key Issues

If you see errors related to API keys:
1. Verify that your `.env` file contains the correct API keys
2. Ensure the environment variables are being loaded properly
3. Check that you have sufficient credits/quota on your OpenAI account

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

```
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
