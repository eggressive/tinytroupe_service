#!/usr/bin/env python3
"""
Final verification that the TinyTroupe service recognizes the API key
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.services.tinytroupe_service import TinyTroupeService

# Test the service initialization
print("=== FINAL VERIFICATION ===")
service = TinyTroupeService()

if service.api_key:
    print("✅ SUCCESS: TinyTroupe service successfully loaded API key")
    print(f"API Key preview: {service.api_key[:20]}...")
else:
    print("❌ FAILED: No API key found")

print(f"Service initialized with {len(service.advisors)} advisors")
