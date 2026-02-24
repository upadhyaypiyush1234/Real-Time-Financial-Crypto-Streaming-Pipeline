# ✅ Your Next Steps

Great! You found your bootstrap server. Here's what to do next:

## Step 1: Create SASL Credentials (2 minutes)

You saw "**Manage credentials**" in your Redpanda console. Click on it!

### What You'll Do:
1. Click "**Manage credentials**" link
2. Click "**Create credentials**" or "**Add user**" button
3. Fill in:
   - **Username**: `crypto-producer` (you can choose any name)
   - **Mechanism**: SCRAM (should already be selected)
4. Click "**Create**" or "**Generate**"
5. **COPY THE PASSWORD IMMEDIATELY!** ⚠️ You won't see it again!

### You'll Get:
```
Username: crypto-producer
Password: abc123xyz... (long random string)
```

---

## Step 2: Update .env File (1 minute)

I've already added your bootstrap server to `.env`. Now add your credentials:

```bash
open -e .env
```

Update these two lines:
```env
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=paste-your-password-here
```

Your `.env` should look like:
```env
KAFKA_BOOTSTRAP_SERVERS=d6benh9dvf8ruqkbmp8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=YourActualPasswordHere
KAFKA_TOPIC=crypto-trades
```

**Save the file!**

---

## Step 3: Get Neon Database (3 minutes)

1. Go to https://neon.tech
2. Sign in with GitHub
3. Click "Create Project"
4. Name: `crypto-pipeline`
5. Copy the connection string
6. Update `DATABASE_URL` in `.env`

---

## Step 4: Initialize Database (1 minute)

```bash
python3 scripts/setup_database.py
```

Expected output:
```
✓ Created trades table
✓ Created trade_aggregates table
✓ Created indexes
Database setup completed successfully!
```

---

## Step 5: Test Your Setup (1 minute)

```bash
python3 test_credentials.py
```

Expected output:
```
✅ Kafka connection successful!
✅ Database connection successful!
✨ All tests passed!
```

---

## Step 6: Run the Pipeline! (2 minutes)

### Terminal 1 - Producer
```bash
python3 src/producer.py
```

Expected:
```
Starting crypto producer...
WebSocket connection opened
Subscribed to streams: ['btcusdt@trade', 'ethusdt@trade']
```

### Terminal 2 - Consumer
```bash
python3 src/consumer.py
```

Expected:
```
Starting crypto consumer...
Processed BTCUSDT: $50000.00 | MA: $50000.00
```

### Terminal 3 - Dashboard
```bash
python3 -m streamlit run src/dashboard.py
```

Browser opens to http://localhost:8501 with live data!

---

## Summary

✅ Bootstrap server: **DONE** (already in .env)
⏳ SASL credentials: Click "Manage credentials" → Create user → Copy password
⏳ Update .env: Add username and password
⏳ Get Neon database: https://neon.tech
⏳ Initialize database: `python3 scripts/setup_database.py`
⏳ Run pipeline: 3 terminals with producer, consumer, dashboard

---

## Your Bootstrap Server (Already Added)

```
d6benh9dvf8ruqkbmp8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
```

This is already in your `.env` file! ✅

---

**You're almost there!** Just create the SASL credentials and you're ready to run! 🚀
