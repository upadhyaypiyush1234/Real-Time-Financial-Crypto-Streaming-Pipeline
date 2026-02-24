# 🔑 Quick Guide: Get Redpanda Credentials

## What You Need

1. **Bootstrap Servers** - The Kafka endpoint
2. **Username** - SASL username (you create this)
3. **Password** - SASL password (generated once)

---

## Step 1: Get Bootstrap Servers

1. Go to https://cloud.redpanda.com
2. Click your cluster name
3. Look for **"Overview"** or **"Connect"** tab
4. Find **"Bootstrap servers"** section
5. Copy the endpoint:
   ```
   seed-abc123.cloud.redpanda.com:9092
   ```

**Can't find it?** Look for:
- "Kafka API endpoint"
- "Seed brokers"
- "Connection string"

---

## Step 2: Create SASL User

1. In your cluster, go to **"Security"** tab
2. Click **"Create User"** button
3. Fill in:
   - **Username**: `crypto-producer`
   - **Mechanism**: **SCRAM-SHA-256**
   - **Permissions**: Read + Write on topic `crypto-trades`
4. Click **"Create"**
5. **COPY THE PASSWORD IMMEDIATELY!** (You won't see it again)

---

## Step 3: Update .env File

```bash
open -e .env
```

Paste your values:

```env
KAFKA_BOOTSTRAP_SERVERS=seed-abc123.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=your-long-password-here
KAFKA_TOPIC=crypto-trades
```

Save the file!

---

## Step 4: Test

```bash
python3 test_credentials.py
```

Should see:
```
✅ Kafka connection successful!
```

---

## Need More Help?

📖 **Detailed Guide**: [HOW_TO_GET_REDPANDA_CREDENTIALS.md](HOW_TO_GET_REDPANDA_CREDENTIALS.md)

This has:
- Screenshots descriptions
- Troubleshooting
- Alternative locations
- Common issues

---

## Quick Troubleshooting

**"Can't find Bootstrap Servers"**
→ Try Overview, Connect, or Getting Started tabs

**"Can't find Security tab"**
→ Look in left sidebar or top tabs for "Security" or "Access Control"

**"Lost my password"**
→ Delete the user and create a new one

**"Connection failed"**
→ Check for typos, extra spaces, or missing :9092 port

---

**You've got this!** 🚀
