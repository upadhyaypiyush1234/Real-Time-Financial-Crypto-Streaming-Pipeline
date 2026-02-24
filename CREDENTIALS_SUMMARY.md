# 🔑 Getting Your Redpanda Credentials - Summary

## What You Need from Redpanda Cloud

### 1. Bootstrap Servers (Kafka Endpoint)
**Where to find it:**
- Log into https://cloud.redpanda.com
- Click your cluster
- Go to "Overview" tab
- Look for "Kafka API" or "Bootstrap servers"

**What it looks like:**
```
seed-abc123.cloud.redpanda.com:9092
```

**Copy this entire string!**

---

### 2. SASL Credentials (Username & Password)
**Where to create it:**
- In your cluster, go to "Security" tab
- Click "Create User"
- Enter username: `crypto-producer`
- Select mechanism: SCRAM-SHA-256
- Click "Create"

**What you'll get:**
```
Username: crypto-producer
Password: AbCdEf123XyZ789LongRandomString
```

**⚠️ IMPORTANT: Copy the password immediately! You won't see it again!**

---

## Put Them in Your .env File

```bash
# Open .env
open -e .env
```

Update these lines:
```env
KAFKA_BOOTSTRAP_SERVERS=seed-abc123.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=AbCdEf123XyZ789LongRandomString
KAFKA_TOPIC=crypto-trades
```

Save the file!

---

## Test Your Credentials

```bash
python3 test_credentials.py
```

If you see `✅ Kafka connection successful!` - you're done!

---

## Need More Help?

- **Quick Visual Guide**: [REDPANDA_CREDENTIALS_QUICK_GUIDE.md](REDPANDA_CREDENTIALS_QUICK_GUIDE.md)
- **Detailed Guide**: [HOW_TO_GET_REDPANDA_CREDENTIALS.md](HOW_TO_GET_REDPANDA_CREDENTIALS.md)
- **Full Setup**: [REDPANDA_SETUP.md](REDPANDA_SETUP.md)

---

**That's all you need!** Two values from Redpanda, paste them in `.env`, and you're ready to go! 🚀
