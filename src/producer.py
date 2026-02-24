"""Kafka producer that ingests live crypto trades from Binance WebSocket."""

import json
import logging
import time
from typing import Dict, Any
import websocket
from kafka import KafkaProducer
from kafka.errors import KafkaError

from config import Config

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CryptoProducer:
    """Producer that streams crypto trades to Kafka."""

    def __init__(self):
        """Initialize the producer."""
        Config.validate()
        self.producer = self._create_producer()
        self.ws = None

    def _create_producer(self) -> KafkaProducer:
        """Create and configure Kafka producer."""
        kafka_config = Config.get_kafka_config()
        return KafkaProducer(
            **kafka_config,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=3,
            max_in_flight_requests_per_connection=1,
        )

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

            # Send to Kafka
            future = self.producer.send(Config.KAFKA_TOPIC, value=trade_event)
            future.add_callback(self._on_send_success)
            future.add_errback(self._on_send_error)

            logger.debug(
                f"Sent trade: {trade_event['symbol']} @ ${trade_event['price']}"
            )

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_send_success(self, record_metadata) -> None:
        """Callback for successful send."""
        logger.debug(
            f"Message sent to {record_metadata.topic} "
            f"partition {record_metadata.partition} "
            f"offset {record_metadata.offset}"
        )

    def _on_send_error(self, exception: Exception) -> None:
        """Callback for send errors."""
        logger.error(f"Failed to send message: {exception}")

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        """Handle WebSocket errors."""
        logger.error(f"WebSocket error: {error}")

    def _on_close(
        self, ws: websocket.WebSocketApp, close_status_code: int, close_msg: str
    ) -> None:
        """Handle WebSocket close."""
        logger.warning(f"WebSocket closed: {close_status_code} - {close_msg}")

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Handle WebSocket open."""
        logger.info("WebSocket connection opened")

        # Subscribe to trade streams
        streams = [f"{symbol.lower()}@trade" for symbol in Config.SYMBOLS]
        subscribe_message = {"method": "SUBSCRIBE", "params": streams, "id": 1}
        ws.send(json.dumps(subscribe_message))
        logger.info(f"Subscribed to streams: {streams}")

    def start(self) -> None:
        """Start the producer."""
        logger.info("Starting crypto producer...")

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
        if self.producer:
            self.producer.flush()
            self.producer.close()
        logger.info("Producer closed")


def main():
    """Main entry point."""
    producer = CryptoProducer()
    producer.start()


if __name__ == "__main__":
    main()
