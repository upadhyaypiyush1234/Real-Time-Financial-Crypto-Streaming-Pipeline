# Real-Time Cryptocurrency Streaming Pipeline

A production-grade data engineering project that demonstrates real-time data processing, streaming architecture, and live visualization of cryptocurrency market data.

## 🎯 Project Overview

This project showcases a complete end-to-end streaming data pipeline that:
- **Ingests** live cryptocurrency trade data from Binance WebSocket API
- **Streams** events through Apache Kafka for reliable message delivery
- **Processes** trades in real-time with moving average calculations and whale trade detection
- **Stores** processed data in PostgreSQL for historical analysis
- **Visualizes** live metrics on an interactive dashboard

## 🏗️ Architecture

```
Binance WebSocket API → Kafka Producer → Kafka Topic → Kafka Consumer → PostgreSQL → Streamlit Dashboard
                                                              ↓
                                                    Real-time Processing
                                                    (Moving Averages, 
                                                     Whale Detection)
```

### Components

1. **Producer** (`src/producer.py`): Connects to Binance WebSocket, receives live BTC/ETH trades, publishes to Kafka
2. **Kafka**: Message broker ensuring reliable, scalable event streaming (Redpanda Cloud)
3. **Consumer** (`src/consumer.py`): Consumes trades from Kafka, calculates metrics, stores in database
4. **PostgreSQL**: Stores trade history and aggregated metrics (Neon serverless)
5. **Dashboard** (`src/dashboard.py`): Real-time visualization with auto-refresh (Streamlit)

## 💡 What I'm Demonstrating

This project showcases my skills in:

- **Distributed Systems**: Event-driven architecture with Kafka for decoupled, scalable components
- **Real-Time Processing**: Stream processing with moving averages and anomaly detection (whale trades >$100k)
- **Data Engineering**: ETL pipeline from ingestion to storage to visualization
- **Cloud Infrastructure**: Serverless deployment using free-tier cloud services
- **Python Development**: Clean, production-ready code with proper error handling and logging
- **DevOps**: Containerization with Docker, automated deployment, monitoring

## 🚀 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Source | Binance WebSocket API | Live cryptocurrency trade data |
| Message Broker | Kafka (Redpanda Cloud) | Event streaming, decoupling |
| Processing | Python 3.11+ | Business logic, calculations |
| Database | PostgreSQL (Neon) | Persistent storage |
| Visualization | Streamlit | Interactive dashboard |
| Deployment | GitHub Codespaces | Cloud runtime |

## ✨ Key Features

- **Real-time ingestion**: Sub-second latency from trade execution to visualization
- **Scalable architecture**: Kafka enables horizontal scaling of producers/consumers
- **Whale trade detection**: Automatically flags large trades (>$100k)
- **Moving averages**: Calculates rolling averages for trend analysis
- **Live dashboard**: Auto-refreshing charts with price, volume, and trade metrics
- **Fault tolerance**: Kafka ensures no data loss, automatic reconnection on failures

## 📊 Dashboard Features

- Live price charts with moving averages
- Trade volume visualization
- Real-time metrics (current price, trade count, volume)
- Whale trade alerts and history
- Multi-symbol support (BTC, ETH)
- Configurable time windows and refresh rates

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Kafka cluster (Redpanda Cloud - free tier)
- PostgreSQL database (Neon - free tier)

### Local Setup

```bash
# Clone repository
git clone https://github.com/upadhyaypiyush1234/Real-Time-Financial-Crypto-Streaming-Pipeline.git
cd Real-Time-Financial-Crypto-Streaming-Pipeline

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
python scripts/setup_database.py

# Run pipeline
./start_pipeline.sh

# View dashboard
streamlit run src/dashboard.py
```

### Cloud Deployment

See [CODESPACES_DEPLOY.md](CODESPACES_DEPLOY.md) for GitHub Codespaces deployment (free, 60 hours/month).

## 📁 Project Structure

```
├── src/
│   ├── producer.py          # Kafka producer (WebSocket → Kafka)
│   ├── consumer.py          # Kafka consumer (Kafka → PostgreSQL)
│   ├── dashboard.py         # Streamlit visualization
│   └── config.py            # Configuration management
├── scripts/
│   └── setup_database.py    # Database schema initialization
├── start_pipeline.sh        # Start producer & consumer
├── stop_pipeline.sh         # Stop all services
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## 🎓 Learning Outcomes

Building this project taught me:
- Designing event-driven architectures
- Working with streaming data and message brokers
- Real-time data processing patterns
- Cloud-native application deployment
- Monitoring and debugging distributed systems

## 📈 Future Enhancements

- [ ] Add more cryptocurrencies (SOL, BNB, ADA)
- [ ] Implement technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Email/SMS alerts for whale trades
- [ ] Machine learning price prediction
- [ ] Historical data analysis and backtesting
- [ ] Kubernetes deployment for production scale

## 📝 License

MIT License - feel free to use this project for learning and portfolio purposes.

## 🔗 Links

- [Live Dashboard](https://your-app.streamlit.app) (coming soon)
- [Architecture Documentation](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)

---

**Built with ❤️ to demonstrate real-time data engineering skills**
