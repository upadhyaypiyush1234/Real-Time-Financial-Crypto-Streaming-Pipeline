# 🚀 Quick Guide: Get Redpanda Credentials in 5 Minutes

## What You Need

Two things:
1. **Bootstrap Servers** (Kafka endpoint)
2. **SASL Credentials** (Username + Password)

---

## Step-by-Step

### 1. Log In
🔗 Go to: https://cloud.redpanda.com

### 2. Click Your Cluster
Click on `crypto-pipeline` (or whatever you named it)

### 3. Get Bootstrap Servers

**Look in the "Overview" tab:**

```
┌─────────────────────────────────────┐
│ Overview                            │
├─────────────────────────────────────┤
│                                     │
│ Kafka API                           │
│ ┌─────────────────────────────────┐ │
│ │ Bootstrap servers:              │ │
│ │ seed-abc.cloud.redpanda.com:9092│ │
│ │                          [Copy] │ │
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

✅ **Copy this!** Example: `seed-abc123.cloud.redpanda.com:9092`

### 4. Create SASL User

**Go to "Security" tab:**

```
┌─────────────────────────────────────┐
│ Security                            │
├─────────────────────────────────────┤
│                                     │
│ [Create User] button                │
│                                     │
└─────────────────────────────────────┘
```

Click "Create User"

### 5. Fill in User Details

```
┌─────────────────────────────────────┐
│ Create User                         │
├─────────────────────────────────────┤
│                                     │
│ Username: [crypto-producer]         │
│                                     │
│ Mechanism: [SCRAM-SHA-256] ▼        │
│                                     │
│ Topic: [crypto-trades]              │
│ Permissions: [Read & Write]         │
│                                     │
│           [Create]                  │
└─────────────────────────────────────┘
```

### 6. Copy Password Immediately!

After clicking "Create", you'll see:

```
┌─────────────────────────────────────┐
│ User Created Successfully!          │
├─────────────────────────────────────┤
│                                     │
│ Username: crypto-producer           │
│                                     │
│ Password: AbCdEf123XyZ789...        │
│           [Copy]                    │
│                                     │
│ ⚠️  Save this password now!         │
│    You won't see it again.          │
│                                     │
│           [Done]                    │
└─────────────────────────────────────┘
```

✅ **Copy the password NOW!**

---

## Update .env File

Open your `.env` file:

```bash
open -e .env
```

Paste your values:

```env
KAFKA_BOOTSTRAP_SERVERS=seed-abc123.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=AbCdEf123XyZ789LongRandomString
KAFKA_TOPIC=crypto-trades
```

Save the file!

---

## Test It

```bash
python3 test_credentials.py
```

If you see:
```
✅ Kafka connection successful!
```

**You're done!** 🎉

---

## Quick Troubleshooting

### Can't find Bootstrap Servers?
- Check "Overview" tab
- Look for "Kafka API" section
- Or check "How to Connect" button

### Can't find Security tab?
- Try "Access Control"
- Or "Users"
- Or "Authentication"

### Lost password?
- Create a new user
- Delete old one if needed
- Copy password immediately this time!

### Credentials don't work?
- Check bootstrap servers ends with `:9092`
- Verify no extra spaces
- Make sure password is complete
- Check mechanism is SCRAM-SHA-256

---

## What Each Credential Looks Like

### Bootstrap Servers
```
seed-grizzly-12345-us1.cloud.redpanda.com:9092
     ↑         ↑      ↑                    ↑
   prefix   cluster region              port
```
- Always ends with `:9092`
- Includes `.cloud.redpanda.com`

### Username
```
crypto-producer
```
- Whatever you chose
- No spaces
- Usually lowercase

### Password
```
YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkw
```
- Long random string
- Mix of letters and numbers
- Case-sensitive

---

## Need More Help?

📖 **Detailed Guide**: [HOW_TO_GET_REDPANDA_CREDENTIALS.md](HOW_TO_GET_REDPANDA_CREDENTIALS.md)

📋 **Full Setup**: [REDPANDA_SETUP.md](REDPANDA_SETUP.md)

❓ **FAQ**: [FAQ.md](FAQ.md)

---

**That's it!** Once you have these three values in your `.env` file, you're ready to run the pipeline! 🚀
