#!/bin/bash

# Stop the crypto streaming pipeline

echo "🛑 Stopping Crypto Streaming Pipeline..."

# Kill producer
if pkill -f "python src/producer.py"; then
    echo "✓ Producer stopped"
else
    echo "ℹ️  Producer was not running"
fi

# Kill consumer
if pkill -f "python src/consumer.py"; then
    echo "✓ Consumer stopped"
else
    echo "ℹ️  Consumer was not running"
fi

echo ""
echo "✅ Pipeline stopped"
