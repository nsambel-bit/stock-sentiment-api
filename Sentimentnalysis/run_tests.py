"""
Test runner script for the Stock Sentiment Analysis API
This script runs both unit tests and integration tests
"""

import subprocess
import sys
import os


def run_unit_tests():
    """Run unit tests using pytest"""
    print("🧪 Running Unit Tests...")
    print("=" * 50)
    
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_sentiment_analyzer.py", 
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running unit tests: {e}")
        return False


def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Running Integration Tests...")
    print("=" * 50)
    
    try:
        # Import and run the integration tests
        from tests.test_api import run_all_tests
        run_all_tests()
        return True
    except Exception as e:
        print(f"Error running integration tests: {e}")
        return False


def run_all_test_suites():
    """Run all test suites"""
    print("""
╔════════════════════════════════════════════════════╗
║        Stock Sentiment Analysis - Test Suite      ║
╚════════════════════════════════════════════════════╝
    """)
    
    # Check if API is running for integration tests
    print("Note: For integration tests to pass, make sure the API is running:")
    print("  python main.py")
    print("  or")
    print("  python app.py")
    print()
    
    # Run unit tests
    unit_tests_passed = run_unit_tests()
    
    # Run integration tests
    integration_tests_passed = run_integration_tests()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Unit Tests: {'✅ PASSED' if unit_tests_passed else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_tests_passed else '❌ FAILED'}")
    
    if unit_tests_passed and integration_tests_passed:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_all_test_suites()
    sys.exit(0 if success else 1)
