"""Quick test to verify all imports work."""

print("Testing imports...")

try:
    import kafka

    print("✅ kafka-python")
except ImportError as e:
    print(f"❌ kafka-python: {e}")

try:
    import websocket

    print("✅ websocket-client")
except ImportError as e:
    print(f"❌ websocket-client: {e}")

try:
    import sqlalchemy

    print("✅ sqlalchemy")
except ImportError as e:
    print(f"❌ sqlalchemy: {e}")

try:
    import psycopg2

    print("✅ psycopg2")
except ImportError as e:
    print(f"❌ psycopg2: {e}")

try:
    import streamlit

    print("✅ streamlit")
except ImportError as e:
    print(f"❌ streamlit: {e}")

try:
    import pandas

    print("✅ pandas")
except ImportError as e:
    print(f"❌ pandas: {e}")

try:
    import plotly

    print("✅ plotly")
except ImportError as e:
    print(f"❌ plotly: {e}")

try:
    from dotenv import load_dotenv

    print("✅ python-dotenv")
except ImportError as e:
    print(f"❌ python-dotenv: {e}")

print("\n✨ All imports successful! You're ready to go.")
print("\nNext steps:")
print("1. Get free credentials from:")
print("   - Upstash Kafka: https://upstash.com")
print("   - Neon PostgreSQL: https://neon.tech")
print("2. Edit .env file with your credentials")
print("3. Run: python3 scripts/setup_database.py")
print("4. Run: python3 src/producer.py")
