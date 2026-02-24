"""Unit tests for the crypto streaming pipeline."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from collections import deque

import sys

sys.path.insert(0, "src")

from consumer import TradeAggregator


class TestTradeAggregator:
    """Test trade aggregation logic."""

    def test_initialization(self):
        """Test aggregator initialization."""
        aggregator = TradeAggregator()
        assert aggregator.price_windows == {}
        assert aggregator.trade_counts == {}
        assert aggregator.total_volume == {}

    def test_add_first_trade(self):
        """Test adding first trade for a symbol."""
        aggregator = TradeAggregator()
        metrics = aggregator.add_trade("BTCUSDT", 50000.0, 0.5)

        assert "BTCUSDT" in aggregator.price_windows
        assert metrics["moving_average"] == 50000.0
        assert metrics["trade_count"] == 1
        assert metrics["total_volume"] == 0.5

    def test_moving_average_calculation(self):
        """Test moving average calculation."""
        aggregator = TradeAggregator()

        # Add multiple trades
        aggregator.add_trade("BTCUSDT", 50000.0, 0.1)
        aggregator.add_trade("BTCUSDT", 51000.0, 0.2)
        metrics = aggregator.add_trade("BTCUSDT", 49000.0, 0.3)

        expected_avg = (50000.0 + 51000.0 + 49000.0) / 3
        assert metrics["moving_average"] == expected_avg
        assert metrics["trade_count"] == 3
        assert metrics["total_volume"] == 0.6

    def test_multiple_symbols(self):
        """Test handling multiple symbols."""
        aggregator = TradeAggregator()

        btc_metrics = aggregator.add_trade("BTCUSDT", 50000.0, 0.5)
        eth_metrics = aggregator.add_trade("ETHUSDT", 3000.0, 1.0)

        assert btc_metrics["moving_average"] == 50000.0
        assert eth_metrics["moving_average"] == 3000.0
        assert len(aggregator.price_windows) == 2

    def test_window_size_limit(self):
        """Test that window respects max size."""
        with patch("consumer.Config.MOVING_AVERAGE_WINDOW", 3):
            aggregator = TradeAggregator()

            # Add more trades than window size
            for i in range(5):
                aggregator.add_trade("BTCUSDT", 50000.0 + i, 0.1)

            # Window should only contain last 3 prices
            assert len(aggregator.price_windows["BTCUSDT"]) == 3


class TestConfig:
    """Test configuration management."""

    def test_kafka_config_format(self):
        """Test Kafka configuration format."""
        from config import Config

        with patch.dict(
            "os.environ",
            {
                "KAFKA_BOOTSTRAP_SERVERS": "test.kafka.com:9092",
                "KAFKA_USERNAME": "testuser",
                "KAFKA_PASSWORD": "testpass",
            },
        ):
            config = Config.get_kafka_config()

            assert config["bootstrap_servers"] == "test.kafka.com:9092"
            assert config["security_protocol"] == "SASL_SSL"
            assert config["sasl_mechanism"] == "SCRAM-SHA-256"
            assert config["sasl_plain_username"] == "testuser"
            assert config["sasl_plain_password"] == "testpass"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
