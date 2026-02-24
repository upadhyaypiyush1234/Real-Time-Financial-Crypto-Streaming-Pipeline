# Deployment Guide

Complete step-by-step guide to deploy the crypto streaming pipeline for free.

## Prerequisites

- GitHub account
- Python 3.11+ installed locally
- Git installed

## Step 1: Set Up Upstash Kafka (Free)

1. Go to https://upstash.com
2. Sign in with GitHub
3. Click "Create Cluster"
4. Select a region close to you
5. Copy the following credentials:
   - Bootstrap Servers (e.g., `xxx.upstash.io:9092`)
   - Username
   - Password
6. Create a topic named `crypto-trades`:
   - Go to Topics tab
   - Click "Create Topic"
   - Name: `crypto-trades`
   - Partitions: 1
   - Retention: 7 days

## Step 2: Set Up Neon PostgreSQL (Free)

1. Go to https://neon.tech
2. Sign in with GitHub
3. Click "Create Project"
4. Name: `crypto-pipeline`
5. Region: Select closest to you
6. Click "Create Project"
7. Copy the connection string (starts with `postgresql://`)
8. Keep this tab open for later

## Step 3: Initialize Database

1. Clone your repository locally:
```bash
git clone <your-repo-url>
cd crypto-streaming-pipeline
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` with your credentials:
```env
KAFKA_BOOTSTRAP_SERVERS=your-cluster.upstash.io:9092
KAFKA_USERNAME=your-username
KAFKA_PASSWORD=your-password
KAFKA_TOPIC=crypto-trades
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
SYMBOLS=BTCUSDT,ETHUSDT
WHALE_THRESHOLD=100000
MOVING_AVERAGE_WINDOW=100
LOG_LEVEL=INFO
```

6. Run database setup:
```bash
python scripts/setup_database.py
```

You should see:
```
✓ Created trades table
✓ Created trade_aggregates table
✓ Created indexes
Database setup completed successfully!
```

## Step 4: Test Locally

1. Terminal 1 - Start Producer:
```bash
cd src
python producer.py
```

You should see:
```
Starting crypto producer...
WebSocket connection opened
Subscribed to streams: ['btcusdt@trade', 'ethusdt@trade']
```

2. Terminal 2 - Start Consumer:
```bash
cd src
python consumer.py
```

You should see:
```
Starting crypto consumer...
Subscribed to topic: crypto-trades
Processed BTCUSDT: $50000.00 | MA: $50000.00
```

3. Terminal 3 - Start Dashboard:
```bash
streamlit run src/dashboard.py
```

Open http://localhost:8501 in your browser.

If you see data flowing, everything works! Press Ctrl+C to stop all processes.

## Step 5: Deploy to GitHub Actions

1. Push code to GitHub:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Add secrets to GitHub:
   - Go to your repository on GitHub
   - Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add each secret:
     - `KAFKA_BOOTSTRAP_SERVERS`
     - `KAFKA_USERNAME`
     - `KAFKA_PASSWORD`
     - `KAFKA_TOPIC`
     - `DATABASE_URL`
     - `SYMBOLS`
     - `WHALE_THRESHOLD`
     - `MOVING_AVERAGE_WINDOW`

3. Enable GitHub Actions:
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

4. Manually trigger workflows:
   - Go to Actions tab
   - Click "Crypto Producer" workflow
   - Click "Run workflow" → "Run workflow"
   - Repeat for "Crypto Consumer" workflow

5. Monitor logs:
   - Click on running workflow
   - Click on job name
   - View real-time logs

**Note**: GitHub Actions has a 6-hour timeout for jobs. For continuous operation, consider:
- Using a free tier cloud service (Railway, Render)
- Running locally on your machine
- Using a Raspberry Pi or old laptop

## Step 6: Deploy Streamlit Dashboard

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file path: `src/dashboard.py`
6. Click "Advanced settings"
7. Add secrets (same as .env file):
```toml
KAFKA_BOOTSTRAP_SERVERS = "your-cluster.upstash.io:9092"
KAFKA_USERNAME = "your-username"
KAFKA_PASSWORD = "your-password"
KAFKA_TOPIC = "crypto-trades"
DATABASE_URL = "postgresql://user:password@host.neon.tech/dbname?sslmode=require"
SYMBOLS = "BTCUSDT,ETHUSDT"
WHALE_THRESHOLD = "100000"
MOVING_AVERAGE_WINDOW = "100"
LOG_LEVEL = "INFO"
```
8. Click "Deploy"

Your dashboard will be live at: `https://your-app-name.streamlit.app`

## Step 7: Verify Everything Works

1. Check Upstash dashboard:
   - Should see messages flowing through topic
   - Monitor throughput and lag

2. Check Neon dashboard:
   - Should see database size growing
   - Monitor query performance

3. Check Streamlit dashboard:
   - Should see live price updates
   - Charts should update automatically
   - Whale trades should appear

## Troubleshooting

### Producer not connecting to Kafka
- Verify Upstash credentials
- Check if topic exists
- Ensure firewall allows outbound connections

### Consumer not processing messages
- Check Kafka topic has messages
- Verify database connection
- Check consumer group is active in Upstash

### Dashboard shows no data
- Verify database has data: `SELECT COUNT(*) FROM trades;`
- Check DATABASE_URL in Streamlit secrets
- Ensure consumer is running

### GitHub Actions failing
- Check secrets are set correctly
- View workflow logs for specific errors
- Ensure requirements.txt is up to date

## Cost Monitoring

All services used are free tier:
- Upstash Kafka: 10k messages/day free
- Neon PostgreSQL: 0.5 GB storage free
- Streamlit Cloud: Unlimited public apps
- GitHub Actions: 2000 minutes/month free

Monitor usage in each dashboard to stay within limits.

## Next Steps

- Add more symbols (ETH, BNB, SOL)
- Implement price alerts
- Add technical indicators (RSI, MACD)
- Create email notifications for whale trades
- Add authentication to dashboard
- Implement data retention policies
