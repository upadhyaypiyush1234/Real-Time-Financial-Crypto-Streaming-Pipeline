"""Database setup script for creating tables and indexes."""

import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import create_engine, text
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_database():
    """Create database tables and indexes."""
    Config.validate()
    engine = create_engine(Config.DATABASE_URL)

    logger.info("Creating database tables...")

    with engine.connect() as conn:
        # Create trades table
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS trades (
                id BIGSERIAL PRIMARY KEY,
                symbol VARCHAR(20) NOT NULL,
                price DECIMAL(20, 8) NOT NULL,
                quantity DECIMAL(20, 8) NOT NULL,
                trade_time TIMESTAMP NOT NULL,
                trade_value DECIMAL(20, 2) NOT NULL,
                is_buyer_maker BOOLEAN NOT NULL,
                moving_average DECIMAL(20, 8),
                is_whale_trade BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """
            )
        )
        logger.info("✓ Created trades table")

        # Create aggregates table
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS trade_aggregates (
                symbol VARCHAR(20) PRIMARY KEY,
                moving_average DECIMAL(20, 8) NOT NULL,
                trade_count BIGINT NOT NULL,
                total_volume DECIMAL(30, 8) NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """
            )
        )
        logger.info("✓ Created trade_aggregates table")

        # Create indexes
        conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_trades_symbol_time 
            ON trades(symbol, trade_time DESC)
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_trades_whale 
            ON trades(is_whale_trade, trade_time DESC) 
            WHERE is_whale_trade = TRUE
        """
            )
        )

        conn.execute(
            text(
                """
            CREATE INDEX IF NOT EXISTS idx_trades_time 
            ON trades(trade_time DESC)
        """
            )
        )

        logger.info("✓ Created indexes")

        conn.commit()

    logger.info("Database setup completed successfully!")


if __name__ == "__main__":
    setup_database()
