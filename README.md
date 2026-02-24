# Real-Time Crypto Data Pipeline

A production-grade streaming data pipeline that ingests live cryptocurrency trades, processes them in real-time, and visualizes metrics on a live dashboard.

## Architecture

```
Binance WebSocket → Kafka (Redpanda) → Consumer → PostgreSQL (Neon) → Streamlit Dashboard
```

## Tech Stack

- **Data Source**: Binance Public WebSocket API
- **Message Broker**: Redpanda Cloud (Kafka-compatible, Serverless)
- **Processing**: Python 3.11+
- **Database**: Neon PostgreSQL (Serverless)
- **Deployment**: GitHub Actions
- **Visualization**: Streamlit Community Cloud

## Features

- Real-time ingestion of BTC/ETH trades
- Kafka-based event streaming
- Whale trade detection (>$100k)
- Moving average calculations
- Live dashboard with auto-refresh

## Quick Start

### Prerequisites
- Python 3.11+
- GitHub account
- Redpanda Cloud account (free, GitHub login)
- Neon account (free, GitHub login)

### Setup (15 minutes)

1. **Get credentials**:
   - **Quick Guide**: [CREDENTIALS_QUICK_GUIDE.md](CREDENTIALS_QUICK_GUIDE.md)
   - **Detailed Guide**: [HOW_TO_GET_REDPANDA_CREDENTIALS.md](HOW_TO_GET_REDPANDA_CREDENTIALS.md)
   - Redpanda Cloud: https://redpanda.com/try-redpanda
   - Neon PostgreSQL: https://neon.tech

2. **Configure**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   open -e .env
   ```

3. **Initialize database**:
   ```bash
   python3 scripts/setup_database.py
   ```

4. **Run the pipeline**:
   ```bash
   # Terminal 1: Producer
   python3 src/producer.py
   
   # Terminal 2: Consumer
   python3 src/consumer.py
   
   # Terminal 3: Dashboard
   python3 -m streamlit run src/dashboard.py
   ```

## Documentation

- **START_WITH_REDPANDA.md** - Quick start guide
- **REDPANDA_SETUP.md** - Detailed setup instructions
- **REDPANDA_CHECKLIST.md** - Step-by-step checklist
- **ARCHITECTURE.md** - System design and architecture
- **DEPLOYMENT.md** - Production deployment guide
- **PROJECT_SUMMARY.md** - Resume tips and talking points
- **FAQ.md** - Frequently asked questions
- **COMMANDS.md** - Command reference

## Project Structure

```
crypto-streaming-pipeline/
├── src/
│   ├── producer.py       # Kafka producer (Binance WebSocket)
│   ├── consumer.py       # Kafka consumer (data processing)
│   ├── dashboard.py      # Streamlit visualization
│   └── config.py         # Configuration management
├── scripts/
│   └── setup_database.py # Database initialization
├── tests/
│   └── test_pipeline.py  # Unit tests
├── .github/
│   └── workflows/
│       ├── producer.yml  # Producer deployment
│       └── consumer.yml  # Consumer deployment
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Monitoring

- Check GitHub Actions for producer/consumer logs
- Monitor Upstash dashboard for Kafka metrics
- View Neon dashboard for database performance

## License

MIT
