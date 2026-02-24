# Useful Commands Reference

Quick reference for common tasks and commands.

## Setup Commands

```bash
# Initial setup
./setup.sh

# Manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Validate setup
python validate.py

# Setup database
python scripts/setup_database.py
```

## Running Locally

```bash
# Using Make
make run-producer    # Terminal 1
make run-consumer    # Terminal 2
make run-dashboard   # Terminal 3

# Direct commands
python src/producer.py
python src/consumer.py
streamlit run src/dashboard.py
```

## Development Commands

```bash
# Run tests
make test
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Format code
make format
black src/ tests/
isort src/ tests/

# Lint code
make lint
flake8 src/ tests/

# Clean temporary files
make clean
```

## Database Commands

```bash
# Connect to Neon database
psql $DATABASE_URL

# Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# Count trades
SELECT symbol, COUNT(*) FROM trades GROUP BY symbol;

# Recent whale trades
SELECT * FROM trades WHERE is_whale_trade = TRUE ORDER BY trade_time DESC LIMIT 10;

# Current aggregates
SELECT * FROM trade_aggregates;

# Delete old data (keep last 7 days)
DELETE FROM trades WHERE trade_time < NOW() - INTERVAL '7 days';
```

## Kafka Commands (Upstash Console)

```bash
# View topic details
# Go to Upstash Console → Topics → crypto-trades

# Check consumer lag
# Go to Upstash Console → Consumer Groups → crypto-consumer-group

# View recent messages
# Go to Upstash Console → Topics → crypto-trades → Messages
```

## Docker Commands

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Git Commands

```bash
# Initial commit
git init
git add .
git commit -m "Initial commit: Real-time crypto streaming pipeline"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main

# Create feature branch
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Update from main
git checkout main
git pull origin main
```

## GitHub Actions

```bash
# Trigger workflow manually
# Go to Actions → Select workflow → Run workflow

# View logs
# Go to Actions → Select run → Select job

# Cancel running workflow
# Go to Actions → Select run → Cancel workflow
```

## Monitoring Commands

```bash
# Watch producer logs
tail -f logs/producer.log

# Watch consumer logs
tail -f logs/consumer.log

# Monitor system resources
htop

# Check Python process
ps aux | grep python

# Kill process
pkill -f producer.py
```

## Debugging Commands

```bash
# Test Kafka connection
python -c "from kafka import KafkaProducer; from config import Config; p = KafkaProducer(**Config.get_kafka_config()); print('Connected!')"

# Test database connection
python -c "from sqlalchemy import create_engine; from config import Config; e = create_engine(Config.DATABASE_URL); e.connect(); print('Connected!')"

# Test WebSocket connection
python -c "import websocket; ws = websocket.create_connection('wss://stream.binance.com:9443/ws/btcusdt@trade'); print(ws.recv()); ws.close()"

# Check environment variables
python -c "from config import Config; Config.validate(); print('Config valid!')"
```

## Performance Testing

```bash
# Measure producer throughput
python -c "
import time
from src.producer import CryptoProducer
start = time.time()
# Run for 60 seconds and count messages
"

# Measure consumer lag
# Check Upstash console for consumer group lag

# Database query performance
EXPLAIN ANALYZE SELECT * FROM trades WHERE symbol = 'BTCUSDT' AND trade_time > NOW() - INTERVAL '1 hour';
```

## Deployment Commands

```bash
# Deploy to Streamlit Cloud
# 1. Push to GitHub
# 2. Go to streamlit.io/cloud
# 3. Click "New app"
# 4. Select repository and branch
# 5. Set main file: src/dashboard.py
# 6. Add secrets
# 7. Click "Deploy"

# Update deployment
git push origin main
# Streamlit Cloud auto-deploys on push

# View deployment logs
# Go to Streamlit Cloud → Your app → Manage app → Logs
```

## Backup Commands

```bash
# Backup database
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql

# Export trades to CSV
psql $DATABASE_URL -c "COPY (SELECT * FROM trades) TO STDOUT WITH CSV HEADER" > trades.csv

# Backup configuration
cp .env .env.backup
```

## Troubleshooting Commands

```bash
# Check if ports are in use
lsof -i :8501  # Streamlit
lsof -i :9092  # Kafka

# Kill process on port
kill -9 $(lsof -t -i:8501)

# Check Python packages
pip list
pip show kafka-python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Useful Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Project aliases
alias crypto-setup='cd ~/crypto-streaming-pipeline && source venv/bin/activate'
alias crypto-producer='cd ~/crypto-streaming-pipeline && source venv/bin/activate && python src/producer.py'
alias crypto-consumer='cd ~/crypto-streaming-pipeline && source venv/bin/activate && python src/consumer.py'
alias crypto-dashboard='cd ~/crypto-streaming-pipeline && source venv/bin/activate && streamlit run src/dashboard.py'
alias crypto-test='cd ~/crypto-streaming-pipeline && source venv/bin/activate && pytest tests/ -v'
```

## Environment Variables

```bash
# View current config
python -c "from config import Config; import pprint; pprint.pprint(vars(Config))"

# Test with different config
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT python src/producer.py

# Override whale threshold
WHALE_THRESHOLD=50000 python src/consumer.py
```

## Quick Checks

```bash
# Is producer running?
ps aux | grep producer.py

# Is consumer running?
ps aux | grep consumer.py

# Is dashboard running?
ps aux | grep streamlit

# Check database connection
python -c "from sqlalchemy import create_engine; from config import Config; create_engine(Config.DATABASE_URL).connect()"

# Check Kafka connection
python -c "from kafka import KafkaConsumer; from config import Config; KafkaConsumer(**Config.get_kafka_config())"
```

## Performance Optimization

```bash
# Create database indexes
psql $DATABASE_URL -c "CREATE INDEX CONCURRENTLY idx_trades_symbol_time ON trades(symbol, trade_time DESC);"

# Analyze database
psql $DATABASE_URL -c "ANALYZE trades;"

# Vacuum database
psql $DATABASE_URL -c "VACUUM ANALYZE;"

# Check slow queries
psql $DATABASE_URL -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```
