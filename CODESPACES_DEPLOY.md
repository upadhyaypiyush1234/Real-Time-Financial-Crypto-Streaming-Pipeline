# Deploy with GitHub Codespaces (Free)

GitHub Codespaces gives you 60 hours/month free - perfect for running your crypto pipeline 24/7 for demos and portfolio.

## Setup (5 minutes)

### 1. Create Codespace

1. Go to your GitHub repo: https://github.com/upadhyaypiyush1234/Real-Time-Financial-Crypto-Streaming-Pipeline
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for codespace to start (1-2 minutes)

### 2. Setup Environment

In the codespace terminal:

```bash
# Install dependencies
pip install -r requirements.txt

# Your .env file should already be there, but verify:
cat .env
```

### 3. Initialize Database (First Time Only)

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

### 4. Start Services

```bash
# Start producer in background
nohup python src/producer.py > producer.log 2>&1 &

# Start consumer in background
nohup python src/consumer.py > consumer.log 2>&1 &

# Check they're running
ps aux | grep python
```

### 5. Monitor Logs

```bash
# Watch producer logs
tail -f producer.log

# Watch consumer logs (in another terminal)
tail -f consumer.log
```

You should see:
- Producer: "WebSocket connection opened", "Subscribed to streams"
- Consumer: "Processed BTCUSDT: $...", "Processed ETHUSDT: $..."

### 6. Run Dashboard Locally

```bash
streamlit run src/dashboard.py
```

Codespaces will forward the port automatically. Click the popup to open the dashboard.

## Keep It Running

### Option A: Keep Codespace Active
- Don't close the browser tab
- Codespace stays active for 30 minutes after last activity
- Free tier: 60 hours/month

### Option B: Stop/Start as Needed
```bash
# Stop services
pkill -f "python src/producer.py"
pkill -f "python src/consumer.py"

# Start again later
nohup python src/producer.py > producer.log 2>&1 &
nohup python src/consumer.py > consumer.log 2>&1 &
```

## Deploy Dashboard to Streamlit Cloud

While producer/consumer run in Codespaces, deploy the dashboard publicly:

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. New app → Select your repo
4. Main file: `src/dashboard.py`
5. Add secrets:
   ```toml
   DATABASE_URL = "postgresql://neondb_owner:npg_bBCIpR3NGK9c@ep-holy-math-aik2zwlo-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
   SYMBOLS = "BTCUSDT,ETHUSDT"
   WHALE_THRESHOLD = "100000"
   MOVING_AVERAGE_WINDOW = "100"
   ```
6. Deploy

Now you have:
- Producer/Consumer: Running in Codespaces (free 60 hrs/month)
- Dashboard: Public URL on Streamlit Cloud (free unlimited)

## Troubleshooting

### Check if services are running
```bash
ps aux | grep python
```

### Check logs for errors
```bash
tail -50 producer.log
tail -50 consumer.log
```

### Restart services
```bash
pkill -f "python src/producer.py"
pkill -f "python src/consumer.py"
nohup python src/producer.py > producer.log 2>&1 &
nohup python src/consumer.py > consumer.log 2>&1 &
```

### Check database has data
```bash
python -c "
from src.config import Config
from sqlalchemy import create_engine, text
engine = create_engine(Config.DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM trades'))
    print(f'Total trades: {result.scalar()}')
"
```

## Cost

- GitHub Codespaces: 60 hours/month FREE
- Streamlit Cloud: Unlimited FREE
- Kafka (Redpanda): 10k messages/day FREE
- PostgreSQL (Neon): 0.5 GB FREE

Total: $0/month for portfolio/demo usage!
