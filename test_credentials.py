"""Test script to verify your Upstash and Neon credentials."""

import sys
import os

# Add src to path
sys.path.insert(0, "src")

print("🔍 Testing Credentials\n")
print("=" * 60)

# Test 1: Check .env file exists
print("\n1. Checking .env file...")
if not os.path.exists(".env"):
    print("❌ .env file not found!")
    print("   Run: cp .env.example .env")
    sys.exit(1)
print("✅ .env file exists")

# Test 2: Load configuration
print("\n2. Loading configuration...")
try:
    from config import Config

    print("✅ Configuration loaded")
except Exception as e:
    print(f"❌ Failed to load config: {e}")
    sys.exit(1)

# Test 3: Check for placeholder values
print("\n3. Checking for placeholder values...")
placeholders_found = []

if "your-cluster" in Config.KAFKA_BOOTSTRAP_SERVERS:
    placeholders_found.append("KAFKA_BOOTSTRAP_SERVERS")
if "your-username" in Config.KAFKA_USERNAME:
    placeholders_found.append("KAFKA_USERNAME")
if "your-password" in Config.KAFKA_PASSWORD:
    placeholders_found.append("KAFKA_PASSWORD")
if "user:password@host" in Config.DATABASE_URL:
    placeholders_found.append("DATABASE_URL")

if placeholders_found:
    print(f"❌ Found placeholder values in: {', '.join(placeholders_found)}")
    print("\n📝 You need to update .env with real credentials!")
    print("\n   Follow these steps:")
    print("   1. Read GET_CREDENTIALS.md")
    print("   2. Get credentials from Upstash and Neon")
    print("   3. Edit .env file with your actual credentials")
    print("   4. Run this script again")
    sys.exit(1)

print("✅ No placeholder values found")

# Test 4: Validate configuration
print("\n4. Validating configuration...")
try:
    Config.validate()
    print("✅ Configuration is valid")
except ValueError as e:
    print(f"❌ Configuration validation failed: {e}")
    sys.exit(1)

# Test 5: Test Kafka connection
print("\n5. Testing Kafka connection...")
try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError

    print("   Connecting to Kafka...")
    producer = KafkaProducer(**Config.get_kafka_config())
    print("✅ Kafka connection successful!")
    producer.close()
except Exception as e:
    print(f"❌ Kafka connection failed: {e}")
    print("\n   Troubleshooting:")
    print("   - Check KAFKA_BOOTSTRAP_SERVERS is correct")
    print("   - Check KAFKA_USERNAME is correct")
    print("   - Check KAFKA_PASSWORD is correct")
    print("   - Verify cluster is running in Redpanda console")
    print("   - Check your internet connection")
    sys.exit(1)

# Test 6: Test database connection
print("\n6. Testing database connection...")
try:
    from sqlalchemy import create_engine, text

    print("   Connecting to database...")
    engine = create_engine(Config.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        result.fetchone()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\n   Troubleshooting:")
    print("   - Check DATABASE_URL is correct")
    print("   - Verify it ends with ?sslmode=require")
    print("   - Check database is active in Neon console")
    print("   - Check your internet connection")
    sys.exit(1)

# All tests passed!
print("\n" + "=" * 60)
print("✨ All tests passed! Your credentials are working!")
print("=" * 60)
print("\n📋 Next steps:")
print("   1. Initialize database: python3 scripts/setup_database.py")
print("   2. Start producer: python3 src/producer.py")
print("   3. Start consumer: python3 src/consumer.py")
print("   4. Start dashboard: python3 -m streamlit run src/dashboard.py")
print("\n🎉 You're ready to go!")
