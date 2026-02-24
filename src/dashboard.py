"""Streamlit dashboard for real-time crypto trade visualization."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import time

from config import Config

# Page configuration
st.set_page_config(
    page_title="Crypto Streaming Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_db_engine():
    """Create database engine."""
    return create_engine(Config.DATABASE_URL)


def fetch_recent_trades(symbol: str, minutes: int = 60) -> pd.DataFrame:
    """Fetch recent trades from database."""
    engine = get_db_engine()
    query = text(
        """
        SELECT 
            trade_time,
            symbol,
            price,
            quantity,
            trade_value,
            moving_average,
            is_whale_trade,
            is_buyer_maker
        FROM trades
        WHERE symbol = :symbol
            AND trade_time >= NOW() - INTERVAL ':minutes minutes'
        ORDER BY trade_time DESC
        LIMIT 1000
    """
    )

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"symbol": symbol, "minutes": minutes})

    return df


def fetch_aggregates() -> pd.DataFrame:
    """Fetch current aggregates."""
    engine = get_db_engine()
    query = text(
        """
        SELECT 
            symbol,
            moving_average,
            trade_count,
            total_volume,
            updated_at
        FROM trade_aggregates
        ORDER BY symbol
    """
    )

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df


def fetch_whale_trades(hours: int = 24) -> pd.DataFrame:
    """Fetch whale trades."""
    engine = get_db_engine()
    query = text(
        """
        SELECT 
            trade_time,
            symbol,
            price,
            quantity,
            trade_value
        FROM trades
        WHERE is_whale_trade = TRUE
            AND trade_time >= NOW() - INTERVAL ':hours hours'
        ORDER BY trade_time DESC
        LIMIT 100
    """
    )

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"hours": hours})

    return df


def plot_price_chart(df: pd.DataFrame, symbol: str):
    """Create price and moving average chart."""
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f"{symbol} Price & Moving Average", "Trade Volume"),
        row_heights=[0.7, 0.3],
    )

    # Price and MA
    fig.add_trace(
        go.Scatter(
            x=df["trade_time"],
            y=df["price"],
            name="Price",
            line=dict(color="#00ff00", width=1),
            mode="lines",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["trade_time"],
            y=df["moving_average"],
            name="Moving Average",
            line=dict(color="#ff6b6b", width=2),
            mode="lines",
        ),
        row=1,
        col=1,
    )

    # Volume
    colors = ["#ff4444" if maker else "#44ff44" for maker in df["is_buyer_maker"]]
    fig.add_trace(
        go.Bar(
            x=df["trade_time"],
            y=df["trade_value"],
            name="Trade Value",
            marker_color=colors,
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Value (USD)", row=2, col=1)

    fig.update_layout(height=600, hovermode="x unified", template="plotly_dark")

    return fig


def main():
    """Main dashboard function."""
    st.title("📈 Real-Time Crypto Streaming Dashboard")
    st.markdown("Live data from Binance via Kafka → PostgreSQL")

    # Sidebar
    st.sidebar.header("Settings")
    auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 1, 30, 5)
    time_window = st.sidebar.selectbox(
        "Time window",
        [5, 15, 30, 60, 120],
        index=3,
        format_func=lambda x: f"{x} minutes",
    )

    # Fetch aggregates
    try:
        agg_df = fetch_aggregates()

        if agg_df.empty:
            st.warning(
                "No data available yet. Make sure producer and consumer are running."
            )
            return

        # Metrics row
        st.subheader("Current Metrics")
        cols = st.columns(len(agg_df))

        for idx, row in agg_df.iterrows():
            with cols[idx]:
                st.metric(
                    label=row["symbol"],
                    value=f"${row['moving_average']:,.2f}",
                    delta=f"{row['trade_count']:,} trades",
                )
                st.caption(f"Volume: {row['total_volume']:,.4f}")

        # Tabs for each symbol
        tabs = st.tabs([row["symbol"] for _, row in agg_df.iterrows()])

        for idx, (_, row) in enumerate(agg_df.iterrows()):
            with tabs[idx]:
                symbol = row["symbol"]

                # Fetch and plot data
                df = fetch_recent_trades(symbol, time_window)

                if not df.empty:
                    fig = plot_price_chart(df, symbol)
                    st.plotly_chart(fig, use_container_width=True)

                    # Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Latest Price", f"${df.iloc[0]['price']:,.2f}")
                    with col2:
                        st.metric("Avg Price", f"${df['price'].mean():,.2f}")
                    with col3:
                        st.metric("Total Volume", f"{df['quantity'].sum():,.4f}")
                    with col4:
                        whale_count = df["is_whale_trade"].sum()
                        st.metric("Whale Trades", f"{whale_count}")
                else:
                    st.info(f"No recent data for {symbol}")

        # Whale trades section
        st.subheader("🐋 Recent Whale Trades (>$100k)")
        whale_df = fetch_whale_trades(24)

        if not whale_df.empty:
            whale_df["trade_value"] = whale_df["trade_value"].apply(
                lambda x: f"${x:,.2f}"
            )
            whale_df["price"] = whale_df["price"].apply(lambda x: f"${x:,.2f}")
            whale_df["quantity"] = whale_df["quantity"].apply(lambda x: f"{x:,.4f}")
            st.dataframe(whale_df, use_container_width=True, hide_index=True)
        else:
            st.info("No whale trades in the last 24 hours")

        # Auto-refresh
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure your database is set up and the consumer is running.")


if __name__ == "__main__":
    main()
