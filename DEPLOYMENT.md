# Deployment Guide

Deploy your crypto streaming pipeline online for free using Render and Streamlit Cloud.

## Prerequisites

- GitHub account with your code pushed
- Upstash Kafka credentials
- Neon PostgreSQL credentials
- Database already initialized (run `python scripts/setup_database.py` locally first)

## Deployment Options

### Option 1: Render (Recommended - Always Running)

Render offers free tier with 750 hours/month per service.

#### Deploy Producer

1. Go to https://render.com and sign in with GitHub
2. Click "New +" → "Background Worker" (NOT Web Service!)
3. Connect your GitHub repository
4. Configure:
   - Name: `crypto-producer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/producer.py`
   - Instance Type: `Free`
5. Add Environment Variables (click "Advanced"):
   ```
   KAFKA_BOOTSTRAP_SERVERS=d6benh9dvf8ruqkbmp8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
   KAFKA_USERNAME=crypto-producer
   KAFKA_PASSWORD=abTUpmkCnKl8TMd7YFJaM83ByNrDTl
   KAFKA_TOPIC=crypto-trades
   SYMBOLS=BTCUSDT,ETHUSDT
   LOG_LEVEL=INFO
   ```
6. Click "Create Background Worker"

#### Deploy Consumer

1. Click "New +" → "Background Worker" (NOT Web Service!)
2. Connect same repository
3. Configure:
   - Name: `crypto-consumer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/consumer.py`
   - Instance Type: `Free`
4. Add Environment Variables:
   ```
   KAFKA_BOOTSTRAP_SERVERS=d6benh9dvf8ruqkbmp8g.any.us-east-1.mpx.prd.cloud.redpanda.com:9092
   KAFKA_USERNAME=crypto-producer
   KAFKA_PASSWORD=abTUpmkCnKl8TMd7YFJaM83ByNrDTl
   KAFKA_TOPIC=crypto-trades
   DATABASE_URL=postgresql://neondb_owner:npg_bBCIpR3NGK9c@ep-holy-math-aik2zwlo-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
   WHALE_THRESHOLD=100000
   MOVING_AVERAGE_WINDOW=100
   LOG_LEVEL=INFO
   ```
5. Click "Create Background Worker"

### Option 2: Railway (Alternative)

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add two services:
   - Service 1: Start Command = `python src/producer.py`
   - Service 2: Start Command = `python src/consumer.py`
5. Add environment variables to each service
6. Deploy

### Deploy Dashboard (Streamlit Cloud)

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `src/dashboard.py`
5. Click "Advanced settings" → Add secrets:
   ```toml
   DATABASE_URL = "postgresql://user:password@host.neon.tech/dbname?sslmode=require"
   SYMBOLS = "BTCUSDT,ETHUSDT"
   WHALE_THRESHOLD = "100000"
   MOVING_AVERAGE_WINDOW = "100"
   ```
6. Click "Deploy"

Your dashboard will be live at: `https://your-app-name.streamlit.app`

## Verify Deployment

1. **Check Producer Logs** (Render/Railway):
   - Should see: "WebSocket connection opened"
   - Should see: "Subscribed to streams"

2. **Check Consumer Logs**:
   - Should see: "Processed BTCUSDT: $..."
   - Should see database writes

3. **Check Dashboard**:
   - Visit your Streamlit URL
   - Should see live price updates
   - Charts should populate with data

4. **Check Upstash Dashboard**:
   - Go to https://console.upstash.com
   - Select your cluster → Topics → crypto-trades
   - Should see messages flowing

5. **Check Neon Dashboard**:
   - Go to https://console.neon.tech
   - Select your project → Tables
   - Run query: `SELECT COUNT(*) FROM trades;`
   - Should see growing count

## Troubleshooting

### Producer/Consumer Not Starting
- Check logs in Render/Railway dashboard
- Verify all environment variables are set
- Ensure credentials are correct

### No Data in Dashboard
- Verify consumer is running and processing messages
- Check database connection: `SELECT * FROM trades LIMIT 10;`
- Ensure Streamlit secrets match your .env

### Render Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- 750 hours/month per service (enough for 24/7 operation)
- If services stop, they auto-restart on next request

## Cost Summary

All services are FREE:
- Render: 750 hours/month per service (2 services = 1500 hours)
- Streamlit Cloud: Unlimited public apps
- Upstash Kafka: 10k messages/day
- Neon PostgreSQL: 0.5 GB storage

## Monitoring

- Render: View logs in dashboard
- Streamlit: Built-in analytics
- Upstash: Message throughput and lag
- Neon: Database size and query performance

## Next Steps

- Add more crypto symbols
- Implement price alerts
- Add technical indicators
- Set up email notifications for whale trades
