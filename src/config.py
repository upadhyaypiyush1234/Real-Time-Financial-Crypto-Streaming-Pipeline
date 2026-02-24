"""Configuration management for the crypto streaming pipeline."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", "")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", "")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "crypto-trades")

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Application Configuration
    SYMBOLS: List[str] = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
    WHALE_THRESHOLD: float = float(os.getenv("WHALE_THRESHOLD", "100000"))
    MOVING_AVERAGE_WINDOW: int = int(os.getenv("MOVING_AVERAGE_WINDOW", "100"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Binance WebSocket
    BINANCE_WS_URL: str = "wss://stream.binance.com:9443/ws"

    @classmethod
    def validate(cls, require_database: bool = True) -> None:
        """Validate required configuration."""
        required = [
            ("KAFKA_BOOTSTRAP_SERVERS", cls.KAFKA_BOOTSTRAP_SERVERS),
            ("KAFKA_USERNAME", cls.KAFKA_USERNAME),
            ("KAFKA_PASSWORD", cls.KAFKA_PASSWORD),
        ]

        if require_database:
            required.append(("DATABASE_URL", cls.DATABASE_URL))

        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

    @classmethod
    def get_kafka_config(cls) -> dict:
        """Get Kafka configuration dictionary."""
        return {
            "bootstrap_servers": cls.KAFKA_BOOTSTRAP_SERVERS,
            "security_protocol": "SASL_SSL",
            "sasl_mechanism": "SCRAM-SHA-256",
            "sasl_plain_username": cls.KAFKA_USERNAME,
            "sasl_plain_password": cls.KAFKA_PASSWORD,
            "request_timeout_ms": 30000,  # 30 seconds for requests
            "api_version_auto_timeout_ms": 10000,  # 10 seconds for API version check
            "connections_max_idle_ms": 540000,  # 9 minutes
            "metadata_max_age_ms": 300000,  # 5 minutes
        }
