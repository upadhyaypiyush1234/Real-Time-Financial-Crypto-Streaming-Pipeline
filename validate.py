"""Validation script to check project setup."""

import sys
import os
from pathlib import Path


def check_file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return Path(filepath).exists()


def check_python_version() -> bool:
    """Check Python version."""
    version = sys.version_info
    return version.major == 3 and version.minor >= 11


def validate_project():
    """Validate project structure and configuration."""
    print("🔍 Validating Crypto Streaming Pipeline")
    print("=" * 50)

    checks = []

    # Python version
    print("\n📋 Checking Python version...")
    if check_python_version():
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        checks.append(True)
    else:
        print(f"❌ Python 3.11+ required. Found: {sys.version_info.major}.{sys.version_info.minor}")
        checks.append(False)

    # Required files
    print("\n📁 Checking required files...")
    required_files = [
        "src/producer.py",
        "src/consumer.py",
        "src/dashboard.py",
        "src/config.py",
        "scripts/setup_database.py",
        "requirements.txt",
        ".env.example",
        "README.md",
    ]

    for filepath in required_files:
        if check_file_exists(filepath):
            print(f"✅ {filepath}")
            checks.append(True)
        else:
            print(f"❌ {filepath} missing")
            checks.append(False)

    # Check .env file
    print("\n⚙️  Checking configuration...")
    if check_file_exists(".env"):
        print("✅ .env file exists")
        checks.append(True)

        # Check if configured
        with open(".env") as f:
            content = f.read()
            if "your-cluster" in content or "your-username" in content:
                print("⚠️  .env file needs configuration")
            else:
                print("✅ .env file appears configured")
    else:
        print("⚠️  .env file not found (run: cp .env.example .env)")
        checks.append(False)

    # Check virtual environment
    print("\n🐍 Checking virtual environment...")
    if check_file_exists("venv") or os.environ.get("VIRTUAL_ENV"):
        print("✅ Virtual environment detected")
        checks.append(True)
    else:
        print("⚠️  Virtual environment not found (run: python -m venv venv)")
        checks.append(False)

    # Try importing dependencies
    print("\n📦 Checking dependencies...")
    try:
        import kafka
        import websocket
        import sqlalchemy
        import streamlit

        print("✅ All dependencies installed")
        checks.append(True)
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        checks.append(False)

    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print("\n✨ Project is ready to run!")
        print("\nNext steps:")
        print("1. Configure .env with your credentials")
        print("2. Run: python scripts/setup_database.py")
        print("3. Start producer: python src/producer.py")
        print("4. Start consumer: python src/consumer.py")
        print("5. Start dashboard: streamlit run src/dashboard.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return False

    return True


if __name__ == "__main__":
    success = validate_project()
    sys.exit(0 if success else 1)
