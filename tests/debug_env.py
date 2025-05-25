#!/usr/bin/env python3
"""
Debug script to check environment variable loading
"""
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Test 1: Check environment before load_dotenv
print("=== BEFORE IMPORTING CONFIG ===")
print(f"OPENAI_API_KEY from os.environ: {os.environ.get('OPENAI_API_KEY', 'NOT_FOUND')}")
print(f"OPENAI_API_KEY from os.getenv: {os.getenv('OPENAI_API_KEY', 'NOT_FOUND')}")

# Test 2: Load dotenv manually
from dotenv import load_dotenv
print("\n=== LOADING .env FILE ===")
env_path = Path(__file__).parent / '.env'
print(f"Loading from: {env_path}")
print(f"File exists: {env_path.exists()}")
result = load_dotenv(env_path)
print(f"load_dotenv result: {result}")

print("\n=== AFTER MANUAL load_dotenv ===")
print(f"OPENAI_API_KEY from os.environ: {os.environ.get('OPENAI_API_KEY', 'NOT_FOUND')}")
print(f"OPENAI_API_KEY from os.getenv: {os.getenv('OPENAI_API_KEY', 'NOT_FOUND')}")

# Test 3: Import config and check Config class
print("\n=== IMPORTING CONFIG CLASS ===")
from config import Config
print(f"Config.OPENAI_API_KEY: {Config.OPENAI_API_KEY}")
print(f"Config.AZURE_OPENAI_API_KEY: {Config.AZURE_OPENAI_API_KEY}")

# Test 4: Check current working directory
print(f"\n=== CURRENT WORKING DIRECTORY ===")
print(f"Current directory: {os.getcwd()}")
print(f"Script directory: {Path(__file__).parent}")
