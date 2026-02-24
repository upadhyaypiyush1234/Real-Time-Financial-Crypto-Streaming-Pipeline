#!/bin/bash

# Start the crypto streaming pipeline in background

echo "🚀 Starting Crypto Streaming Pipeline..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your credentials"
    exit 1
fi

# Install dependencies if needed
if ! python -c "import kafka" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Kill any existing processes
pkill -f "python src/producer.py" 2>/dev/null
pkill -f "python src/consumer.py" 2>/dev/null

# Start producer in background
echo "▶️  Starting producer..."
nohup python src/producer.py > logs/producer.log 2>&1 &
PRODUCER_PID=$!
echo "Producer started (PID: $PRODUCER_PID)"

# Wait a bit for producer to initialize
sleep 3

# Start consumer in background
echo "▶️  Starting consumer..."
nohup python src/consumer.py > logs/consumer.log 2>&1 &
CONSUMER_PID=$!
echo "Consumer started (PID: $CONSUMER_PID)"

echo ""
echo "✅ Pipeline is running!"
echo ""
echo "📊 View logs:"
echo "  Producer: tail -f logs/producer.log"
echo "  Consumer: tail -f logs/consumer.log"
echo ""
echo "🛑 Stop pipeline:"
echo "  ./stop_pipeline.sh"
echo ""
echo "💡 Start dashboard:"
echo "  streamlit run src/dashboard.py"
