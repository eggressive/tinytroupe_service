# Managing Advisors in TinyTroupe Financial Service

This document provides detailed instructions for adding, removing, or modifying advisor personas in your TinyTroupe Financial Advisors service.

## Table of Contents

1. [Understanding Advisor Structure](#understanding-advisor-structure)
2. [Adding a New Advisor](#adding-a-new-advisor)
3. [Removing an Existing Advisor](#removing-an-existing-advisor)
4. [Modifying an Existing Advisor](#modifying-an-existing-advisor)
5. [Updating the Database](#updating-the-database)
6. [Resetting the Database](#resetting-the-database)
7. [Advanced Advisor Management](#advanced-advisor-management)

## Understanding Advisor Structure

Advisors in the TinyTroupe service are represented by the `Persona` model with the following attributes:

- `id`: Unique identifier (e.g., 'warren_buffett')
- `name`: Display name (e.g., 'Warren Buffett')
- `description`: Brief description of the advisor
- `personality`: JSON object containing personality traits and characteristics
- `expertise`: JSON array of expertise areas

The default advisors are defined in `src/config.py` in the `DEFAULT_ADVISORS` list.

## Adding a New Advisor

### Method 1: Using Python Script

Create a Python script to add a new advisor:

```python
# add_advisor.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.models import Persona

# Define the new advisor
new_advisor = {
    'id': 'bill_gates',
    'name': 'Bill Gates',
    'description': 'Microsoft co-founder, philanthropist, and technology visionary.',
    'personality': {
        'traits': ['analytical', 'strategic', 'philanthropic', 'visionary'],
        'communication_style': 'clear and methodical'
    },
    'expertise': ['technology trends', 'business strategy', 'philanthropy', 'global health']
}

# Add to database
with app.app_context():
    # Check if advisor already exists
    existing = Persona.query.filter_by(id=new_advisor['id']).first()
    if existing:
        print(f"Advisor with ID '{new_advisor['id']}' already exists.")
        sys.exit(1)
    
    # Create new advisor
    advisor = Persona(
        id=new_advisor['id'],
        name=new_advisor['name'],
        description=new_advisor['description'],
        personality=new_advisor['personality'],
        expertise=new_advisor['expertise']
    )
    
    db.session.add(advisor)
    db.session.commit()
    print(f"Added new advisor: {new_advisor['name']}")
```

Run the script:

```bash
python add_advisor.py
```

### Method 2: Modifying Configuration

1. Open `src/config.py`
2. Find the `DEFAULT_ADVISORS` list in the `Config` class
3. Add your new advisor to the list:

```python
DEFAULT_ADVISORS = [
    # Existing advisors...
    
    # New advisor
    {
        'id': 'bill_gates',
        'name': 'Bill Gates',
        'description': 'Microsoft co-founder, philanthropist, and technology visionary.',
        'expertise': ['technology trends', 'business strategy', 'philanthropy', 'global health']
    },
]
```

After modifying the configuration, you'll need to [update the database](#updating-the-database) to reflect these changes.

## Removing an Existing Advisor

### Method 1: Using Python Script

Create a Python script to remove an advisor:

```python
# remove_advisor.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.models import Persona

# Advisor ID to remove
advisor_id = 'warren_buffett'  # Replace with the ID you want to remove

# Remove from database
with app.app_context():
    advisor = Persona.query.filter_by(id=advisor_id).first()
    if not advisor:
        print(f"Advisor with ID '{advisor_id}' not found.")
        sys.exit(1)
    
    name = advisor.name
    db.session.delete(advisor)
    db.session.commit()
    print(f"Removed advisor: {name}")
```

Run the script:

```bash
python remove_advisor.py
```

### Method 2: Modifying Configuration

1. Open `src/config.py`
2. Find the `DEFAULT_ADVISORS` list in the `Config` class
3. Remove or comment out the advisor you want to remove:

```python
DEFAULT_ADVISORS = [
    # Removed advisor
    # {
    #     'id': 'warren_buffett',
    #     'name': 'Warren Buffett',
    #     'description': 'The most successful investor of modern times.',
    #     'expertise': ['value investing', 'business analysis', 'capital allocation']
    # },
    
    # Remaining advisors...
]
```

After modifying the configuration, you'll need to [update the database](#updating-the-database) to reflect these changes.

## Modifying an Existing Advisor

### Method 1: Using Python Script

Create a Python script to modify an advisor:

```python
# modify_advisor.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.models import Persona

# Advisor ID to modify
advisor_id = 'albert_einstein'  # Replace with the ID you want to modify

# Updated information
updated_info = {
    'name': 'Albert Einstein',  # Can keep the same or change
    'description': 'Theoretical physicist with unique insights into complex systems and pattern recognition.',
    'personality': {
        'traits': ['curious', 'imaginative', 'analytical', 'intuitive'],
        'communication_style': 'thoughtful and metaphorical'
    },
    'expertise': ['pattern recognition', 'systems thinking', 'thought experiments', 'risk assessment']
}

# Update in database
with app.app_context():
    advisor = Persona.query.filter_by(id=advisor_id).first()
    if not advisor:
        print(f"Advisor with ID '{advisor_id}' not found.")
        sys.exit(1)
    
    advisor.name = updated_info['name']
    advisor.description = updated_info['description']
    advisor.personality = updated_info['personality']
    advisor.expertise = updated_info['expertise']
    
    db.session.commit()
    print(f"Updated advisor: {advisor.name}")
```

Run the script:

```bash
python modify_advisor.py
```

### Method 2: Modifying Configuration

1. Open `src/config.py`
2. Find the `DEFAULT_ADVISORS` list in the `Config` class
3. Modify the advisor's information:

```python
DEFAULT_ADVISORS = [
    # Other advisors...
    
    # Modified advisor
    {
        'id': 'albert_einstein',
        'name': 'Albert Einstein',
        'description': 'Theoretical physicist with unique insights into complex systems and pattern recognition.',
        'expertise': ['pattern recognition', 'systems thinking', 'thought experiments', 'risk assessment']
    },
    
    # Other advisors...
]
```

After modifying the configuration, you'll need to [update the database](#updating-the-database) to reflect these changes.

## Updating the Database

When you modify the `DEFAULT_ADVISORS` list in the configuration, you need to update the database to reflect these changes. There are two approaches:

### Method 1: Selective Update

This script updates the database to match the configuration without losing existing conversation data:

```python
# update_advisors.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.models import Persona
from src.config import Config

with app.app_context():
    # Get current advisors from database
    current_advisors = {advisor.id: advisor for advisor in Persona.query.all()}
    
    # Get configured advisors
    config_advisors = {advisor['id']: advisor for advisor in Config.DEFAULT_ADVISORS}
    
    # Remove advisors that are in database but not in config
    for advisor_id in list(current_advisors.keys()):
        if advisor_id not in config_advisors:
            print(f"Removing advisor: {current_advisors[advisor_id].name}")
            db.session.delete(current_advisors[advisor_id])
    
    # Add or update advisors from config
    for advisor_id, advisor_config in config_advisors.items():
        if advisor_id in current_advisors:
            # Update existing advisor
            advisor = current_advisors[advisor_id]
            advisor.name = advisor_config['name']
            advisor.description = advisor_config['description']
            advisor.expertise = advisor_config['expertise']
            print(f"Updated advisor: {advisor.name}")
        else:
            # Add new advisor
            advisor = Persona(
                id=advisor_id,
                name=advisor_config['name'],
                description=advisor_config['description'],
                personality={'traits': ['analytical'], 'communication_style': 'clear'},  # Default
                expertise=advisor_config['expertise']
            )
            db.session.add(advisor)
            print(f"Added advisor: {advisor_config['name']}")
    
    db.session.commit()
    print("Database updated successfully.")
```

Run the script:

```bash
python update_advisors.py
```

### Method 2: Manual SQL Updates

You can also use SQL commands to update the database directly:

```bash
# Open SQLite database
sqlite3 tinytroupe.db

# Delete an advisor
DELETE FROM personas WHERE id = 'warren_buffett';

# Add a new advisor (simplified example)
INSERT INTO personas (id, name, description, personality, expertise) 
VALUES ('bill_gates', 'Bill Gates', 'Microsoft co-founder and philanthropist', 
'{"traits": ["analytical"]}', '["technology", "business strategy"]');

# Exit SQLite
.exit
```

## Resetting the Database

If you want to completely reset the database to match the current configuration:

### Method 1: Drop and Recreate

```python
# reset_database.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, db
from src.services.conversation_service import ConversationService

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("Dropped all database tables.")
    
    # Recreate tables
    db.create_all()
    print("Recreated database tables.")
    
    # Initialize with default advisors
    conversation_service = ConversationService()
    print("Database reset complete.")
```

Run the script:

```bash
python reset_database.py
```

### Method 2: Delete Database File

For SQLite databases, you can simply delete the database file and restart the application:

```bash
# Stop the application first
rm tinytroupe.db
# Restart the application, which will recreate the database
python src/main.py
```

⚠️ **Warning**: This will delete all conversations and persona states. Only use this method if you want to start fresh.

## Advanced Advisor Management

For more advanced advisor management, consider implementing:

### Admin Interface

Create a web-based admin interface for managing advisors without code changes:

1. Add a new route in `src/main.py`:
   ```python
   @app.route('/admin/advisors')
   def admin_advisors():
       return render_template('admin/advisors.html')
   ```

2. Create templates for listing, adding, editing, and deleting advisors

3. Add corresponding API endpoints in a new file `src/routes/admin.py`

### Advisor Templates Library

Create a library of pre-configured advisors that users can choose from:

1. Create a JSON file with advisor templates:
   ```json
   {
     "financial_experts": [
       {
         "id": "warren_buffett",
         "name": "Warren Buffett",
         "description": "...",
         "expertise": ["..."]
       },
       // More financial experts
     ],
     "tech_visionaries": [
       {
         "id": "bill_gates",
         "name": "Bill Gates",
         "description": "...",
         "expertise": ["..."]
       },
       // More tech visionaries
     ]
   }
   ```

2. Add functions to load these templates and add them to the database

### Dynamic Loading System

Implement a system to load advisor configurations from external files:

1. Create a directory for advisor configurations:
   ```bash
   mkdir -p advisors/enabled
   mkdir -p advisors/available
   ```

2. Add a function to scan the `enabled` directory and load all advisor configurations found there

3. Add a CLI command to enable/disable advisors by creating symlinks between the directories
