# 🔑 How to Get Redpanda Credentials

Step-by-step guide with exact locations to find your credentials.

---

## Part 1: Get Bootstrap Servers (Kafka Endpoint)

### Step 1: Log into Redpanda Console
1. Go to https://cloud.redpanda.com
2. Sign in with your account

### Step 2: Select Your Cluster
1. You'll see your cluster listed (e.g., "crypto-pipeline")
2. Click on the cluster name

### Step 3: Find Bootstrap Servers
Look for one of these sections:

**Option A: "Overview" Tab**
1. Click "Overview" in the left sidebar
2. Look for a section called:
   - "Kafka API" or
   - "Bootstrap servers" or
   - "Connection details"
3. You'll see something like:
   ```
   seed-abc123.cloud.redpanda.com:9092
   ```
4. Click the copy icon or select and copy this text

**Option B: "How to Connect" Section**
1. Look for a "How to Connect" or "Connect" button
2. Click it
3. You'll see connection details
4. Copy the bootstrap servers endpoint

**What it looks like:**
```
Bootstrap servers: seed-abc123-us1.cloud.redpanda.com:9092
```

✅ **Copy this entire string** - you'll need it for your `.env` file!

---

## Part 2: Create SASL Credentials (Username & Password)

### Step 1: Go to Security Tab
1. In your cluster, look at the left sidebar
2. Click on one of these:
   - "Security" or
   - "Access Control" or
   - "Users" or
   - "SASL"

### Step 2: Create New User
1. Click a button that says:
   - "Create User" or
   - "Add User" or
   - "Create SASL Credentials" or
   - "New User"

### Step 3: Configure User
You'll see a form with these fields:

**Username:**
- Enter: `crypto-producer` (or any name you want)

**Mechanism:**
- Select: `SCRAM-SHA-256`
- (This is usually the default or only option)

**Permissions/ACLs (if asked):**
- Topic: `crypto-trades`
- Permissions: Read & Write
- (Some versions auto-grant all permissions)

### Step 4: Create and Copy Password
1. Click "Create" or "Generate"
2. **IMPORTANT**: A password will be shown **ONLY ONCE**
3. You'll see something like:
   ```
   Username: crypto-producer
   Password: AbCdEf123XyZ789LongRandomString
   ```
4. **COPY THE PASSWORD IMMEDIATELY!**
5. Save it somewhere safe (you'll paste it in `.env` file)

⚠️ **WARNING**: If you close this window without copying the password, you'll need to create a new user!

---

## Part 3: Update Your .env File

Now that you have both pieces of information, update your `.env` file:

```bash
# Open .env file
open -e .env
```

Update these lines:

```env
# Replace with YOUR actual values:
KAFKA_BOOTSTRAP_SERVERS=seed-abc123-us1.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=AbCdEf123XyZ789LongRandomString
KAFKA_TOPIC=crypto-trades
```

**Save the file!**

---

## Visual Guide: Where to Look

### Redpanda Console Layout

```
┌─────────────────────────────────────────────────────┐
│  Redpanda Cloud                          [Profile]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐                                   │
│  │ Left Sidebar│                                   │
│  ├─────────────┤                                   │
│  │ Overview    │ ← Look here for Bootstrap Servers│
│  │ Topics      │                                   │
│  │ Connectors  │                                   │
│  │ Security    │ ← Look here for SASL Credentials │
│  │ Monitoring  │                                   │
│  │ Settings    │                                   │
│  └─────────────┘                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Common Locations by Redpanda Version

### Newer Redpanda Console
- **Bootstrap Servers**: Overview → "Kafka API" section
- **SASL Credentials**: Security → "Users" → "Create User"

### Older Redpanda Console
- **Bootstrap Servers**: Cluster Details → "Connection Info"
- **SASL Credentials**: Access Control → "SASL" → "Add Credentials"

---

## Troubleshooting

### "I can't find Bootstrap Servers"
Try these locations:
1. Overview tab → Look for "Kafka API" or "Connection details"
2. Click your cluster name → Look for connection info
3. Settings → Connection details
4. Look for any section mentioning "Kafka" or "Bootstrap"

### "I can't find Security/SASL section"
Try these:
1. Look for "Security" in left sidebar
2. Look for "Access Control"
3. Look for "Users"
4. Look for "Authentication"
5. Check cluster settings

### "I lost my password"
Unfortunately, you can't retrieve it. You need to:
1. Go back to Security/Users
2. Delete the old user (if allowed)
3. Create a new user
4. Copy the new password immediately

### "My credentials don't work"
Check these:
1. Bootstrap servers includes `:9092` at the end
2. No extra spaces in username or password
3. Password is complete (they're usually long)
4. Mechanism is SCRAM-SHA-256
5. User has permissions on topic `crypto-trades`

---

## Example Values

Here's what your credentials should look like:

```env
# Example (yours will be different):
KAFKA_BOOTSTRAP_SERVERS=seed-grizzly-12345-us1.cloud.redpanda.com:9092
KAFKA_USERNAME=crypto-producer
KAFKA_PASSWORD=YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkw
KAFKA_TOPIC=crypto-trades
```

**Key points:**
- Bootstrap servers ends with `:9092`
- Username is what you chose (e.g., `crypto-producer`)
- Password is a long random string
- Topic name is `crypto-trades`

---

## Test Your Credentials

After updating `.env`, test them:

```bash
python3 test_credentials.py
```

Expected output:
```
✅ Kafka connection successful!
```

If you see this, your credentials are correct! 🎉

If you see an error, double-check:
1. Bootstrap servers is correct
2. Username is correct
3. Password is correct (no extra spaces)
4. All values are in `.env` file

---

## Quick Checklist

- [ ] Logged into Redpanda Cloud
- [ ] Found cluster
- [ ] Copied bootstrap servers (ends with :9092)
- [ ] Created SASL user
- [ ] Copied username
- [ ] Copied password (immediately!)
- [ ] Updated `.env` file
- [ ] Saved `.env` file
- [ ] Tested with `python3 test_credentials.py`

---

## Still Stuck?

If you're still having trouble:

1. **Take a screenshot** of your Redpanda console
2. Look for anything that says:
   - "Kafka API"
   - "Bootstrap"
   - "Connection"
   - "Security"
   - "SASL"
   - "Users"
3. Check the [REDPANDA_SETUP.md](REDPANDA_SETUP.md) guide
4. Check [FAQ.md](FAQ.md) for common issues

---

**Remember**: The bootstrap servers and SASL credentials are the two most important pieces of information you need from Redpanda. Take your time finding them! 🔍
