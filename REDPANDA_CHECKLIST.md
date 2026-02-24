# ✅ Redpanda Setup Checklist

Follow this step-by-step to get your full Kafka pipeline running!

## Pre-Setup
- [ ] Python 3.11+ installed
- [ ] All dependencies installed (`python3 test_imports.py` passes)
- [ ] Project files ready

## Redpanda Cloud Setup

### Account & Cluster
- [ ] Go to https://redpanda.com/try-redpanda
- [ ] Create account (email or GitHub)
- [ ] Verify email if required
- [ ] Create cluster (Serverless, AWS, closest region)
- [ ] Wait for cluster to be ready (~2-3 minutes)

### Topic Creation
- [ ] Click on your cluster
- [ ] Go to "Topics" tab
- [ ] Create topic: `crypto-trades`
- [ ] Partitions: 1
- [ ] Confirm topic is created

### Get Credentials
- [ ] Go to "Security" or "Access Control"
- [ ] Create SASL user: `crypto-producer`
- [ ] Mechanism: SCRAM-SHA-256
- [ ] **COPY PASSWORD IMMEDIATELY** (you won't see it again!)
- [ ] Go to "Overview" or "Connect"
- [ ] Copy Bootstrap servers (e.g., `seed-abc123.cloud.redpanda.com:9092`)

## Neon PostgreSQL Setup

- [ ] Go to https://neon.tech
- [ ] Sign in with GitHub
- [ ] Create project: `crypto-pipeline`
- [ ] Copy connection string
- [ ] Keep tab open for reference

## Configuration

- [ ] Open `.env` file: `open -e .env`
- [ ] Update `KAFKA_BOOTSTRAP_SERVERS` with Redpanda endpoint
- [ ] Update `KAFKA_USERNAME` with your username
- [ ] Update `KAFKA_PASSWORD` with your password
- [ ] Update `DATABASE_URL` with Neon connection string
- [ ] Save file
- [ ] Double-check no extra spaces or quotes

## Database Setup

- [ ] Run: `python3 scripts/setup_database.py`
- [ ] See: ✓ Created trades table
- [ ] See: ✓ Created trade_aggregates table
- [ ] See: ✓ Created indexes
- [ ] See: Database setup completed successfully!

## Test Credentials

- [ ] Run: `python3 test_credentials.py`
- [ ] See: ✅ Kafka connection successful!
- [ ] See: ✅ Database connection successful!
- [ ] See: ✨ All tests passed!

## Run the Pipeline

### Terminal 1: Producer
- [ ] Run: `python3 src/producer.py`
- [ ] See: Starting crypto producer...
- [ ] See: WebSocket connection opened
- [ ] See: Subscribed to streams
- [ ] Leave running

### Terminal 2: Consumer
- [ ] Open new terminal
- [ ] Run: `python3 src/consumer.py`
- [ ] See: Starting crypto consumer...
- [ ] See: Subscribed to topic: crypto-trades
- [ ] See: Processed BTCUSDT messages
- [ ] Leave running

### Terminal 3: Dashboard
- [ ] Open new terminal
- [ ] Run: `python3 -m streamlit run src/dashboard.py`
- [ ] Browser opens to http://localhost:8501
- [ ] See live data in metrics
- [ ] See charts updating
- [ ] See whale trades section

## Verification

### Redpanda Console
- [ ] Go to Redpanda console
- [ ] Check "Topics" → `crypto-trades`
- [ ] See message count increasing
- [ ] Check "Consumer Groups"
- [ ] See `crypto-consumer-group` active

### Neon Console
- [ ] Go to Neon console
- [ ] Open SQL Editor
- [ ] Run: `SELECT COUNT(*) FROM trades;`
- [ ] See count increasing
- [ ] Run: `SELECT * FROM trade_aggregates;`
- [ ] See BTC and ETH data

### Dashboard
- [ ] Metrics show current prices
- [ ] Charts are displaying
- [ ] Data is updating (watch for 5 seconds)
- [ ] Multiple symbols visible
- [ ] Whale trades appearing (if any >$100k)

## Success Criteria

✅ Producer running without errors
✅ Consumer processing messages
✅ Dashboard showing live data
✅ Data flowing: Binance → Redpanda → Consumer → Database → Dashboard
✅ No errors in any terminal

## If Something Fails

### Producer Issues
1. Check Redpanda credentials in `.env`
2. Verify cluster is running
3. Check internet connection
4. See REDPANDA_SETUP.md troubleshooting

### Consumer Issues
1. Make sure producer is running first
2. Check topic exists in Redpanda
3. Verify database connection
4. Check consumer logs for errors

### Dashboard Issues
1. Make sure consumer is running
2. Check database has data
3. Verify DATABASE_URL in `.env`
4. Clear browser cache

## Next Steps After Success

- [ ] Let it run for 30 minutes to collect data
- [ ] Take screenshots for portfolio
- [ ] Update resume with project
- [ ] Push code to GitHub
- [ ] Deploy dashboard to Streamlit Cloud
- [ ] Add to LinkedIn

## Quick Commands

```bash
# Test imports
python3 test_imports.py

# Test credentials
python3 test_credentials.py

# Setup database
python3 scripts/setup_database.py

# Run producer
python3 src/producer.py

# Run consumer (new terminal)
python3 src/consumer.py

# Run dashboard (new terminal)
python3 -m streamlit run src/dashboard.py

# Check database
# In Neon SQL Editor:
SELECT COUNT(*) FROM trades;
SELECT * FROM trade_aggregates;
```

## Resources

- **Setup Guide**: REDPANDA_SETUP.md
- **Redpanda Console**: https://cloud.redpanda.com
- **Neon Console**: https://console.neon.tech
- **Redpanda Docs**: https://docs.redpanda.com
- **Project FAQ**: FAQ.md

---

**You've got this!** Follow the checklist and you'll have a full Kafka pipeline running in 20 minutes. 🚀
