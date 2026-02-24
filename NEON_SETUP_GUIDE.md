# 🗄️ Neon PostgreSQL Setup Guide

Quick guide to set up your free PostgreSQL database on Neon.

## Step 1: Create Neon Account (1 minute)

1. Go to https://neon.tech
2. Click **"Sign in with GitHub"**
3. Authorize Neon to access your GitHub account
4. You'll be redirected to Neon Console

## Step 2: Create a Project (2 minutes)

1. You'll see a **"Create Project"** or **"New Project"** button
2. Click it
3. Fill in:
   - **Project Name**: `crypto-pipeline`
   - **Database Name**: `neondb` (default, keep it)
   - **Region**: Choose same as Redpanda (e.g., `us-east-1`)
   - **PostgreSQL Version**: 16 (default, keep it)
4. Click **"Create Project"**

## Step 3: Get Connection String (1 minute)

After project is created, you'll see a **Connection String**:

### Look for "Connection String" Section

You'll see something like:
```
postgresql://username:password@ep-cool-name-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Copy the Entire String

There's usually a **"Copy"** button next to it.

**Important**: Make sure it includes `?sslmode=require` at the end!

## Step 4: Update Your .env File (1 minute)

```bash
open -e .env
```

Update the DATABASE_URL line:
```env
DATABASE_URL=postgresql://username:password@ep-cool-name-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Save the file!**

## Step 5: Initialize Database (1 minute)

Run the setup script:
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

## ✅ That's It!

Your Neon database is ready!

---

## What You Get from Neon

- **Connection String**: The full PostgreSQL URL
- **Free Tier**: 0.5 GB storage (plenty for this project)
- **Auto-scaling**: Database scales automatically
- **Serverless**: No maintenance required

---

## Troubleshooting

### "Can't find connection string"

Look for these sections in Neon Console:
- "Connection Details"
- "Connection String"
- "Quick Start"
- "Connect"

### "Multiple connection strings shown"

You might see:
- **Pooled connection** ← Use this one!
- Direct connection
- Internal connection

Choose **"Pooled connection"** for best performance.

### "Connection string doesn't have ?sslmode=require"

Add it manually:
```
postgresql://user:pass@host.neon.tech/neondb?sslmode=require
                                                ↑ Add this part
```

---

## Quick Reference

### What You Need from Neon:
1. Connection string (starts with `postgresql://`)
2. Must include `?sslmode=require` at the end

### Where It Goes:
In your `.env` file:
```env
DATABASE_URL=postgresql://your-connection-string-here
```

### Test It:
```bash
python3 scripts/setup_database.py
```

---

## Visual Guide

### Neon Console Layout

```
┌─────────────────────────────────────────┐
│  Neon Console                           │
├─────────────────────────────────────────┤
│                                         │
│  Projects                               │
│  ┌─────────────────────────────────┐   │
│  │ crypto-pipeline                 │   │
│  │                                 │   │
│  │ Connection String:              │   │
│  │ postgresql://user:pass@...      │   │
│  │                         [Copy]  │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## After Setup

Once database is initialized, you can:

1. **View your data** in Neon Console:
   - Go to "SQL Editor" tab
   - Run: `SELECT * FROM trades LIMIT 10;`

2. **Monitor storage**:
   - Check "Dashboard" for storage usage
   - Free tier: 0.5 GB

3. **Check tables**:
   - `trades` - stores all trade data
   - `trade_aggregates` - stores calculated metrics

---

## Summary

1. ✅ Go to https://neon.tech
2. ✅ Sign in with GitHub
3. ✅ Create project: `crypto-pipeline`
4. ✅ Copy connection string
5. ✅ Update `.env` with DATABASE_URL
6. ✅ Run `python3 scripts/setup_database.py`

**Done!** Your database is ready for the pipeline! 🎉
