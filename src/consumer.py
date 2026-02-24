"""Kafka consumer that processes trades and stores aggregated data."""

import json
import logging
from collections import deque
from typing import Dict, Deque
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import Config

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class TradeAggregator:
    """Aggregates trade data and calculates metrics."""

    def __init__(self):
        """Initialize aggregator."""
        self.price_windows: Dict[str, Deque[float]] = {}
        self.trade_counts: Dict[str, int] = {}
        self.total_volume: Dict[str, float] = {}

    def add_trade(self, symbol: str, price: float, quantity: float) -> Dict:
        """Add trade and calculate metrics."""
        # Initialize symbol tracking
        if symbol not in self.price_windows:
            self.price_windows[symbol] = deque(maxlen=Config.MOVING_AVERAGE_WINDOW)
            self.trade_counts[symbol] = 0
            self.total_volume[symbol] = 0.0

        # Update metrics
        self.price_windows[symbol].append(price)
        self.trade_counts[symbol] += 1
        self.total_volume[symbol] += quantity

        # Calculate moving average
        moving_avg = sum(self.price_windows[symbol]) / len(self.price_windows[symbol])

        return {
            "moving_average": moving_avg,
            "trade_count": self.trade_counts[symbol],
            "total_volume": self.total_volume[symbol],
        }


class CryptoConsumer:
    """Consumer that processes trades and stores data."""

    def __init__(self):
        """Initialize consumer."""
        Config.validate()
        self.consumer = self._create_consumer()
        self.engine = create_engine(Config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.aggregator = TradeAggregator()

    def _create_consumer(self) -> KafkaConsumer:
        """Create and configure Kafka consumer."""
        kafka_config = Config.get_kafka_config()
        return KafkaConsumer(
            Config.KAFKA_TOPIC,
            **kafka_config,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id="crypto-consumer-group-v2",  # New group to start fresh
        )

    def _store_trade(self, trade: Dict, metrics: Dict) -> None:
        """Store trade data in database."""
        session = self.Session()
        try:
            query = text(
                """
                INSERT INTO trades (
                    symbol, price, quantity, trade_time, trade_value,
                    is_buyer_maker, moving_average, is_whale_trade
                ) VALUES (
                    :symbol, :price, :quantity, 
                    to_timestamp(:trade_time / 1000.0),
                    :trade_value, :is_buyer_maker, :moving_average, :is_whale_trade
                )
            """
            )

            session.execute(
                query,
                {
                    "symbol": trade["symbol"],
                    "price": trade["price"],
                    "quantity": trade["quantity"],
                    "trade_time": trade["trade_time"],
                    "trade_value": trade["trade_value"],
                    "is_buyer_maker": trade["is_buyer_maker"],
                    "moving_average": metrics["moving_average"],
                    "is_whale_trade": trade["trade_value"] >= Config.WHALE_THRESHOLD,
                },
            )
            session.commit()

        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def _update_aggregates(self, symbol: str, metrics: Dict) -> None:
        """Update aggregate statistics table."""
        session = self.Session()
        try:
            query = text(
                """
                INSERT INTO trade_aggregates (
                    symbol, moving_average, trade_count, total_volume, updated_at
                ) VALUES (
                    :symbol, :moving_average, :trade_count, :total_volume, NOW()
                )
                ON CONFLICT (symbol) DO UPDATE SET
                    moving_average = EXCLUDED.moving_average,
                    trade_count = EXCLUDED.trade_count,
                    total_volume = EXCLUDED.total_volume,
                    updated_at = EXCLUDED.updated_at
            """
            )

            session.execute(
                query,
                {
                    "symbol": symbol,
                    "moving_average": metrics["moving_average"],
                    "trade_count": metrics["trade_count"],
                    "total_volume": metrics["total_volume"],
                },
            )
            session.commit()

        except Exception as e:
            logger.error(f"Aggregate update error: {e}")
            session.rollback()
        finally:
            session.close()

    def start(self) -> None:
        """Start consuming messages."""
        logger.info("Starting crypto consumer...")
        logger.info(f"Subscribed to topic: {Config.KAFKA_TOPIC}")

        try:
            for message in self.consumer:
                trade = message.value

                # Calculate metrics
                metrics = self.aggregator.add_trade(
                    trade["symbol"], trade["price"], trade["quantity"]
                )

                # Store in database
                self._store_trade(trade, metrics)
                self._update_aggregates(trade["symbol"], metrics)

                # Log whale trades
                if trade["trade_value"] >= Config.WHALE_THRESHOLD:
                    logger.warning(
                        f"🐋 WHALE TRADE: {trade['symbol']} "
                        f"${trade['trade_value']:,.2f} @ ${trade['price']}"
                    )

                logger.info(
                    f"Processed {trade['symbol']}: "
                    f"${trade['price']:.2f} | MA: ${metrics['moving_average']:.2f}"
                )

        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            self.close()

    def close(self) -> None:
        """Close consumer connections."""
        if self.consumer:
            self.consumer.close()
        logger.info("Consumer closed")


def main():
    """Main entry point."""
    consumer = CryptoConsumer()
    consumer.start()


if __name__ == "__main__":
    main()
