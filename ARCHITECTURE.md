# System Architecture

## Overview

This project implements a real-time data streaming pipeline using event-driven architecture principles. It demonstrates industry-standard patterns for handling high-throughput data streams.

## Architecture Diagram

```
┌─────────────────┐
│  Binance API    │
│  (WebSocket)    │
└────────┬────────┘
         │ Live Trades
         ▼
┌─────────────────┐
│    Producer     │
│  (Python App)   │
└────────┬────────┘
         │ JSON Events
         ▼
┌─────────────────┐
│  Upstash Kafka  │
│  (Message Bus)  │
└────────┬────────┘
         │ Stream
         ▼
┌─────────────────┐
│    Consumer     │
│  (Python App)   │
└────────┬────────┘
         │ Processed Data
         ▼
┌─────────────────┐
│  Neon Postgres  │
│   (Database)    │
└────────┬────────┘
         │ Queries
         ▼
┌─────────────────┐
│   Streamlit     │
│   (Dashboard)   │
└─────────────────┘
```

## Components

### 1. Data Source (Binance WebSocket)

**Purpose**: Real-time cryptocurrency trade data

**Technology**: WebSocket API

**Data Format**:
```json
{
  "s": "BTCUSDT",
  "p": "50000.00",
  "q": "0.5",
  "T": 1234567890,
  "m": true
}
```

**Characteristics**:
- High frequency (100+ trades/second)
- Low latency (<100ms)
- Public, no authentication required

### 2. Producer (src/producer.py)

**Purpose**: Ingest trades and publish to Kafka

**Responsibilities**:
- Maintain WebSocket connection
- Parse trade events
- Serialize to JSON
- Publish to Kafka topic
- Handle reconnections

**Key Features**:
- Auto-reconnect on disconnect
- Graceful error handling
- Configurable symbols
- Structured logging

**Performance**:
- Throughput: 1000+ messages/second
- Latency: <10ms per message
- Memory: ~50MB

### 3. Message Broker (Upstash Kafka)

**Purpose**: Decouple producers from consumers

**Configuration**:
- Topic: `crypto-trades`
- Partitions: 1
- Retention: 7 days
- Replication: 3 (managed by Upstash)

**Benefits**:
- Buffering during consumer downtime
- Multiple consumers can read same data
- Replay capability
- Horizontal scalability

**Guarantees**:
- At-least-once delivery
- Ordering within partition
- Durability (replicated)

### 4. Consumer (src/consumer.py)

**Purpose**: Process trades and store results

**Responsibilities**:
- Read from Kafka topic
- Calculate moving averages
- Detect whale trades
- Store in database
- Update aggregates

**Processing Logic**:
```python
1. Receive trade event
2. Update price window (last N prices)
3. Calculate moving average
4. Detect if whale trade (>$100k)
5. Insert into trades table
6. Upsert aggregates table
```

**Key Features**:
- Stateful processing (moving average)
- Idempotent writes
- Error recovery
- Consumer group management

**Performance**:
- Throughput: 500+ messages/second
- Latency: ~50ms per message
- Memory: ~100MB

### 5. Database (Neon PostgreSQL)

**Purpose**: Persistent storage for processed data

**Schema**:

```sql
-- Raw trades
CREATE TABLE trades (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    price DECIMAL(20, 8),
    quantity DECIMAL(20, 8),
    trade_time TIMESTAMP,
    trade_value DECIMAL(20, 2),
    is_buyer_maker BOOLEAN,
    moving_average DECIMAL(20, 8),
    is_whale_trade BOOLEAN,
    created_at TIMESTAMP
);

-- Aggregated metrics
CREATE TABLE trade_aggregates (
    symbol VARCHAR(20) PRIMARY KEY,
    moving_average DECIMAL(20, 8),
    trade_count BIGINT,
    total_volume DECIMAL(30, 8),
    updated_at TIMESTAMP
);
```

**Indexes**:
- `idx_trades_symbol_time`: Fast symbol + time queries
- `idx_trades_whale`: Fast whale trade queries
- `idx_trades_time`: Fast time-based queries

**Optimization**:
- Partitioning by time (future enhancement)
- Materialized views for aggregates
- Connection pooling

### 6. Dashboard (src/dashboard.py)

**Purpose**: Real-time visualization

**Features**:
- Live price charts
- Moving average overlay
- Trade volume bars
- Whale trade alerts
- Auto-refresh

**Technology**:
- Streamlit (UI framework)
- Plotly (interactive charts)
- SQLAlchemy (database queries)

**Update Frequency**: 5 seconds (configurable)

## Data Flow

### Normal Operation

1. **Ingestion** (Producer):
   ```
   WebSocket → Parse → Serialize → Kafka
   ```

2. **Streaming** (Kafka):
   ```
   Topic Buffer → Consumer Group → Delivery
   ```

3. **Processing** (Consumer):
   ```
   Deserialize → Aggregate → Transform → Store
   ```

4. **Visualization** (Dashboard):
   ```
   Query → Transform → Render → Display
   ```

### Error Scenarios

**Producer Failure**:
- WebSocket auto-reconnects
- Kafka buffers messages
- No data loss

**Consumer Failure**:
- Kafka retains messages
- Consumer resumes from last offset
- Reprocesses missed messages

**Database Failure**:
- Consumer retries with backoff
- Kafka prevents message loss
- Manual intervention may be needed

**Kafka Failure**:
- Producer buffers locally (limited)
- Consumer waits for reconnection
- Upstash handles replication

## Scalability

### Current Capacity

- **Throughput**: 1000 trades/second
- **Storage**: 100M trades (~10GB)
- **Latency**: End-to-end <1 second

### Scaling Strategies

**Horizontal Scaling**:
- Add more consumer instances
- Increase Kafka partitions
- Shard database by symbol

**Vertical Scaling**:
- Increase consumer memory
- Optimize database queries
- Use faster storage

**Optimization**:
- Batch database writes
- Use connection pooling
- Implement caching layer

## Monitoring

### Key Metrics

**Producer**:
- Messages sent/second
- WebSocket disconnects
- Kafka send errors

**Kafka**:
- Topic lag
- Partition throughput
- Consumer group status

**Consumer**:
- Messages processed/second
- Processing latency
- Database write errors

**Database**:
- Query performance
- Storage usage
- Connection count

### Alerting

- Kafka lag > 1000 messages
- Consumer processing time > 1 second
- Database storage > 80%
- Producer disconnected > 5 minutes

## Security

### Authentication

- Kafka: SASL/SCRAM-SHA-256
- Database: SSL/TLS required
- Dashboard: Public (add auth for production)

### Data Protection

- Credentials in environment variables
- Secrets in GitHub Actions
- SSL for all connections
- No PII in logs

### Best Practices

- Rotate credentials regularly
- Use least privilege access
- Monitor for anomalies
- Keep dependencies updated

## Future Enhancements

1. **Multi-region deployment**
2. **Real-time alerting system**
3. **Machine learning predictions**
4. **Historical data analysis**
5. **API for external access**
6. **Advanced technical indicators**
7. **Portfolio tracking**
8. **Price alerts via email/SMS**
