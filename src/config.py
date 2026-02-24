"""Configuration management for the crypto streaming pipeline."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Try to load Streamlit secrets if available
try:
    import streamlit as st

    _use_streamlit_secrets = hasattr(st, "secrets") and len(st.secrets) > 0
except (ImportError, FileNotFoundError):
    _use_streamlit_secrets = False


class Config:
    """Application configuration."""

    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", "")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", "")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "crypto-trades")

    # Database Configuration - try Streamlit secrets first, then env
    if _use_streamlit_secrets:
        try:
            import streamlit as st

            DATABASE_URL: str = st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL", ""))
            SYMBOLS: List[str] = st.secrets.get(
                "SYMBOLS", os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT")
            ).split(",")
            WHALE_THRESHOLD: float = float(
                st.secrets.get("WHALE_THRESHOLD", os.getenv("WHALE_THRESHOLD", "100000"))
            )
            MOVING_AVERAGE_WINDOW: int = int(
                st.secrets.get("MOVING_AVERAGE_WINDOW", os.getenv("MOVING_AVERAGE_WINDOW", "100"))
            )
        except:
            DATABASE_URL: str = os.getenv("DATABASE_URL", "")
            SYMBOLS: List[str] = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
            WHALE_THRESHOLD: float = float(os.getenv("WHALE_THRESHOLD", "100000"))
            MOVING_AVERAGE_WINDOW: int = int(os.getenv("MOVING_AVERAGE_WINDOW", "100"))
    else:
        DATABASE_URL: str = os.getenv("DATABASE_URL", "")
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
