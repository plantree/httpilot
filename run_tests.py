"""Test runner script with comprehensive test reporting."""

import subprocess
import sys
import os
import json
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        return result.returncode == 0
    
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def main():
    """Run comprehensive test suite."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("HTTPilot Comprehensive Test Suite")
    print("==================================")
    
    # Test commands to run
    test_commands = [
        # Basic test run
        (["python", "-m", "pytest", "tests/", "-v"], "Basic test run"),
        
        # Test with coverage
        (["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing"], "Test with coverage"),
        
        # Test specific modules
        (["python", "-m", "pytest", "tests/test_basic.py", "-v"], "Basic functionality tests"),
        (["python", "-m", "pytest", "tests/test_http_methods.py", "-v"], "HTTP methods tests"),
        (["python", "-m", "pytest", "tests/test_status_codes.py", "-v"], "Status codes tests"),
        (["python", "-m", "pytest", "tests/test_cache.py", "-v"], "Cache tests"),
        (["python", "-m", "pytest", "tests/test_cookies.py", "-v"], "Cookie tests"),
        (["python", "-m", "pytest", "tests/test_dynamic_data.py", "-v"], "Dynamic data tests"),
        (["python", "-m", "pytest", "tests/test_image.py", "-v"], "Image tests"),
        (["python", "-m", "pytest", "tests/test_redirect.py", "-v"], "Redirect tests"),
        (["python", "-m", "pytest", "tests/test_response_format.py", "-v"], "Response format tests"),
        (["python", "-m", "pytest", "tests/test_response_inspect.py", "-v"], "Response inspection tests"),
        (["python", "-m", "pytest", "tests/test_inspect.py", "-v"], "Request inspection tests"),
        (["python", "-m", "pytest", "tests/test_integration.py", "-v"], "Integration tests"),
        
        # Performance and stress tests
        (["python", "-m", "pytest", "tests/test_integration.py::test_concurrent_requests", "-v"], "Concurrent request tests"),
        (["python", "-m", "pytest", "tests/test_integration.py::test_memory_usage_stability", "-v"], "Memory stability tests"),
        
        # Generate coverage report
        (["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=html", "--cov-report=xml"], "Generate coverage reports"),
    ]
    
    results = []
    
    for cmd, description in test_commands:
        success = run_command(cmd, description)
        results.append((description, success))
        
        if not success:
            print(f"❌ FAILED: {description}")
        else:
            print(f"✅ PASSED: {description}")
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {description}")
    
    print(f"\nTotal: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} test suite(s) failed!")
        return 1
    else:
        print("\n🎉 All test suites passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())