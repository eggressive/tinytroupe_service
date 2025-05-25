#!/usr/bin/env python3
"""
Test script to verify TinyTroupe service API key loading
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

print("=== TESTING TINYTROUPE SERVICE API KEY LOADING ===")

try:
    from src.services.tinytroupe_service import TinyTroupeService
    
    # Create an instance of the service
    service = TinyTroupeService()
    
    print(f"API Key loaded: {'Yes' if service.api_key else 'No'}")
    if service.api_key:
        print(f"API Key (first 10 chars): {service.api_key[:10]}...")
        print("✅ TinyTroupe service successfully loaded API key!")
    else:
        print("❌ TinyTroupe service failed to load API key")
        
except Exception as e:
    print(f"❌ Error importing or initializing TinyTroupe service: {e}")
    import traceback
    traceback.print_exc()
