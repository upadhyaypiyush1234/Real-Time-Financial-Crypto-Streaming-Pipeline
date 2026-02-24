# Real-Time Crypto Data Pipeline

A production-grade streaming data pipeline that ingests live cryptocurrency trades, processes them in real-time, and visualizes metrics on a live dashboard.

## Architecture

```
Binance WebSocket → Kafka (Upstash) → Consumer → PostgreSQL (Neon) → Streamlit Dashboard
```

## Tech Stack

- **Data Source**: Binance Public WebSocket API
- **Message Broker**: Upstash Kafka (Serverless, Free Tier)
- **Processing**: Python 3.11+
- **Database**: Neon PostgreSQL (Serverless, Free Tier)
- **Deployment**: Render + Streamlit Cloud (Free)
- **Visualization**: Streamlit

## Features

- Real-time ingestion of BTC/ETH trades
- Kafka-based event streaming
- Whale trade detection (>$100k)
- Moving average calculations
- Live dashboard with auto-refresh

## Quick Start

### 1. Setup Services (10 minutes)

**Upstash Kafka** (Free):
- Go to https://upstash.com → Sign in with GitHub
- Create Cluster → Copy Bootstrap Servers, Username, Password
- Create Topic: `crypto-trades`

**Neon PostgreSQL** (Free):
- Go to https://neon.tech → Sign in with GitHub
- Create Project → Copy connection string

### 2. Initialize Database

```bash
# Clone and setup
git clone https://github.com/upadhyaypiyush1234/Real-Time-Financial-Crypto-Streaming-Pipeline.git
cd Real-Time-Financial-Crypto-Streaming-Pipeline

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python scripts/setup_database.py
```

### 3. Test Locally

```bash
# Terminal 1: Producer
python src/producer.py

# Terminal 2: Consumer
python src/consumer.py

# Terminal 3: Dashboard
streamlit run src/dashboard.py
```

Visit http://localhost:8501 to see the dashboard.

## Deploy Online (Free)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions using:
- Render (Producer & Consumer)
- Streamlit Cloud (Dashboard)

## Project Structure

```
├── src/
│   ├── producer.py       # Kafka producer (Binance WebSocket)
│   ├── consumer.py       # Kafka consumer (data processing)
│   ├── dashboard.py      # Streamlit visualization
│   └── config.py         # Configuration management
├── scripts/
│   └── setup_database.py # Database initialization
├── Dockerfile.producer   # Producer container
├── Dockerfile.consumer   # Consumer container
├── requirements.txt
└── .env.example
```

## License

MIT
