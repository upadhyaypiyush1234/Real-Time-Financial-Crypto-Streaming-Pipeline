"""Simplified producer that writes directly to database (no Kafka needed)."""

import json
import logging
import time
from typing import Dict
import websocket
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from collections import deque

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
        self.price_windows: Dict[str, deque] = {}
        self.trade_counts: Dict[str, int] = {}
        self.total_volume: Dict[str, float] = {}

    def add_trade(self, symbol: str, price: float, quantity: float) -> Dict:
        """Add trade and calculate metrics."""
        if symbol not in self.price_windows:
            self.price_windows[symbol] = deque(maxlen=Config.MOVING_AVERAGE_WINDOW)
            self.trade_counts[symbol] = 0
            self.total_volume[symbol] = 0.0

        self.price_windows[symbol].append(price)
        self.trade_counts[symbol] += 1
        self.total_volume[symbol] += quantity

        moving_avg = sum(self.price_windows[symbol]) / len(self.price_windows[symbol])

        return {
            "moving_average": moving_avg,
            "trade_count": self.trade_counts[symbol],
            "total_volume": self.total_volume[symbol],
        }


class SimpleCryptoProducer:
    """Producer that streams crypto trades directly to database."""

    def __init__(self):
        """Initialize the producer."""
        Config.validate()
        self.engine = create_engine(Config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.aggregator = TradeAggregator()
        self.ws = None

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

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)

            # Extract trade data
            trade_event = {
                "symbol": data["s"],
                "price": float(data["p"]),
                "quantity": float(data["q"]),
                "trade_time": data["T"],
                "is_buyer_maker": data["m"],
                "trade_value": float(data["p"]) * float(data["q"]),
            }

            # Calculate metrics
            metrics = self.aggregator.add_trade(
                trade_event["symbol"], trade_event["price"], trade_event["quantity"]
            )

            # Store in database
            self._store_trade(trade_event, metrics)
            self._update_aggregates(trade_event["symbol"], metrics)

            # Log whale trades
            if trade_event["trade_value"] >= Config.WHALE_THRESHOLD:
                logger.warning(
                    f"🐋 WHALE TRADE: {trade_event['symbol']} "
                    f"${trade_event['trade_value']:,.2f} @ ${trade_event['price']}"
                )

            logger.debug(
                f"Processed {trade_event['symbol']}: "
                f"${trade_event['price']} | MA: ${metrics['moving_average']:.2f}"
            )

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        """Handle WebSocket errors."""
        logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
        """Handle WebSocket close."""
        logger.warning(f"WebSocket closed: {close_status_code} - {close_msg}")

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Handle WebSocket open."""
        logger.info("WebSocket connection opened")
        logger.info(f"Streaming {', '.join(Config.SYMBOLS)} trades to database")

    def start(self) -> None:
        """Start the producer."""
        logger.info("Starting simplified crypto producer (no Kafka needed)...")
        logger.info("This version writes directly to the database")

        # Build WebSocket URL
        streams = "/".join([f"{symbol.lower()}@trade" for symbol in Config.SYMBOLS])
        ws_url = f"{Config.BINANCE_WS_URL}/{streams}"

        # Create WebSocket connection
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )

        # Run forever with auto-reconnect
        while True:
            try:
                self.ws.run_forever()
                logger.warning("WebSocket disconnected, reconnecting in 5 seconds...")
                time.sleep(5)
            except KeyboardInterrupt:
                logger.info("Shutting down producer...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(5)

        self.close()

    def close(self) -> None:
        """Close producer connections."""
        if self.ws:
            self.ws.close()
        logger.info("Producer closed")


def main():
    """Main entry point."""
    producer = SimpleCryptoProducer()
    producer.start()


if __name__ == "__main__":
    main()
