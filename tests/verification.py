#!/usr/bin/env python3
"""
Final verification script to test all components of the TinyTroupe service
"""
import sys
import os
import requests
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_environment_variables():
    """Test that environment variables are loaded correctly"""
    print("=== Testing Environment Variables ===")
    try:
        from dotenv import load_dotenv
        env_path = project_root / '.env'
        result = load_dotenv(env_path)
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"✅ OPENAI_API_KEY loaded successfully (preview: {api_key[:20]}...)")
            return True
        else:
            print("❌ OPENAI_API_KEY not found")
            return False
    except Exception as e:
        print(f"❌ Error loading environment variables: {e}")
        return False

def test_config_loading():
    """Test that the Config class loads variables correctly"""
    print("\n=== Testing Config Class ===")
    try:
        from src.config import Config
        if Config.OPENAI_API_KEY:
            print(f"✅ Config.OPENAI_API_KEY loaded successfully")
            return True
        else:
            print("❌ Config.OPENAI_API_KEY is None")
            return False
    except Exception as e:
        print(f"❌ Error importing Config: {e}")
        return False

def test_tinytroupe_service():
    """Test that TinyTroupe service initializes correctly"""
    print("\n=== Testing TinyTroupe Service ===")
    try:
        from src.services.tinytroupe_service import TinyTroupeService
        service = TinyTroupeService()
        
        if service.api_key:
            print("✅ TinyTroupe service initialized with API key")
            return True
        else:
            print("❌ TinyTroupe service initialized without API key")
            return False
    except Exception as e:
        print(f"❌ Error initializing TinyTroupe service: {e}")
        return False

def test_flask_app():
    """Test that Flask app can start (check if already running)"""
    print("\n=== Testing Flask Application ===")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running and accessible")
            return True
        else:
            print(f"⚠️  Flask application returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Flask application is not running (this is okay if you haven't started it)")
        return None
    except Exception as e:
        print(f"❌ Error testing Flask application: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🔍 TinyTroupe Service - Final Verification")
    print("=" * 50)
    
    results = []
    results.append(test_environment_variables())
    results.append(test_config_loading())
    results.append(test_tinytroupe_service())
    flask_result = test_flask_app()
    if flask_result is not None:
        results.append(flask_result)
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY:")
    
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests PASSED!")
        print("🎉 TinyTroupe service is ready for use!")
    else:
        failed = total - passed
        print(f"⚠️  {passed}/{total} tests passed, {failed} failed")
        print("🔧 Please review the failed tests above")
    
    if flask_result is None:
        print("\n💡 To test the Flask application, run:")
        print("   source venv/bin/activate")
        print("   python -m src.main")

if __name__ == "__main__":
    main()
