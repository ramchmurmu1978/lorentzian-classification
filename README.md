# Lorentzian Classification Trading System

> **A Python-based machine learning and quantitative trading research system for BTCUSD using Lorentzian Distance, technical feature engineering, historical backtesting, risk management, and Delta Exchange paper-trading infrastructure.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy)](https://numpy.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/)
[![Trading](https://img.shields.io/badge/Trading-Paper%20Trading-orange)](#)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)](#)

---

## Overview

The **Lorentzian Classification Trading System** is an end-to-end Python project designed to investigate whether **Lorentzian-distance-based nearest-neighbour classification** can be used to identify potentially similar market conditions in BTCUSD price data.

The system combines:

- Financial time-series data processing
- Technical indicator engineering
- Lorentzian distance
- Nearest-neighbour classification
- Trading signal generation
- Historical backtesting
- Profit and risk analysis
- Stop Loss / Take Profit management
- Delta Exchange market-data integration
- Virtual/paper-trading infrastructure

The project is being developed incrementally, with each component validated before progressing to the next stage.

> **Important:** This project is currently restricted to research, historical backtesting, and virtual/paper trading. Real-money order execution has not been implemented.

---

# Project Objective

The primary objective is to build a complete and modular algorithmic trading research pipeline:

```text
Market Data
     │
     ▼
Data Validation
     │
     ▼
Feature Engineering
     │
     ├── RSI
     ├── CCI
     ├── WaveTrend
     ├── +DI
     ├── -DI
     └── ADX
     │
     ▼
Lorentzian Distance
     │
     ▼
Nearest-Neighbor Classification
     │
     ▼
Trading Signal
     │
     ├───────────────┐
     ▼               ▼
Backtesting     Paper Trading
     │               │
     ▼               ▼
Performance      Virtual P&L
Evaluation       & Trade Log
     │
     ▼
Strategy Optimization
```

---

# Why Lorentzian Distance?

Traditional distance metrics such as Euclidean distance can be heavily influenced by large differences between individual feature values.

This project investigates **Lorentzian distance** as an alternative similarity measure for financial feature vectors.

The implemented distance function is:

```python
def lorentzian_distance(x, y):
    return np.sum(np.log1p(np.abs(x - y)))
```

Conceptually:

\[
D(x,y) = \sum_i \log(1 + |x_i-y_i|)
\]

The logarithmic transformation reduces the influence of large individual feature differences while preserving relative similarity.

The classifier then searches for historical market states that are closest to the current market state.

---

# Feature Engineering

The model currently uses seven technical features.

| Feature | Description |
|---|---|
| RSI | Relative Strength Index — momentum |
| CCI | Commodity Channel Index — price deviation |
| WT1 | WaveTrend main oscillator |
| WT2 | WaveTrend signal line |
| +DI | Positive Directional Indicator |
| -DI | Negative Directional Indicator |
| ADX | Average Directional Index — trend strength |

The final feature vector is:

```text
[rsi, cci, wt1, wt2, plus_di, minus_di, adx]
```

The same feature-engineering functions are reused for both historical analysis and live market-data processing.

This reduces the risk of introducing differences between the backtesting and live-trading pipelines.

---

# Dataset

The current historical development dataset is:

```text
data/raw/BTCUSD_1h.csv
```

### Dataset Characteristics

| Property | Value |
|---|---:|
| Rows | 1,009 |
| Columns | 6 |
| Missing Values | 0 |
| Duplicate Timestamps | 0 |
| Frequency | 1 Hour |
| Start | 2025-09-12 00:00:00 |
| End | 2025-10-24 00:00:00 |

### Raw Columns

```text
close
high
low
open
time
volume
```

The dataset was validated for:

- Missing values
- Duplicate timestamps
- Chronological ordering
- Valid OHLCV structure
- Time range consistency

---

# Classification Pipeline

The classifier follows this process:

```text
Current Market State
        │
        ▼
Current Feature Vector
        │
        ▼
Calculate Lorentzian Distance
        │
        ▼
Compare Against Historical Feature Vectors
        │
        ▼
Select Nearest Neighbours
        │
        ▼
Majority Vote
        │
        ▼
Trading Prediction
```

The current prediction convention is:

```text
 1  → Long / Bullish
-1  → Short / Bearish
```

---

# Historical Validation

The classification model was validated against historical BTCUSD data.

### Validation Results

| Metric | Result |
|---|---:|
| Total Predictions | 989 |
| Correct Predictions | 574 |
| Incorrect Predictions | 411 |
| Accuracy | **58.27%** |

Prediction distribution:

```text
-1 : 651
 1 : 334
```

### Confusion Matrix

```text
                 Predicted
                 -1      1
Actual   -1      375    135
          1      276    199
```

The project does **not** treat classification accuracy as the sole measure of strategy quality.

For trading systems, profitability, drawdown, consistency and risk-adjusted performance are more important than prediction accuracy alone.

---

# Backtesting Engine

A custom Python backtesting engine was developed to evaluate the generated trading signals.

The engine supports:

- Long positions
- Short positions
- Position reversal
- Position sizing
- Entry and exit prices
- Trade-level P&L
- Capital tracking
- Trade logging
- Stop Loss
- Take Profit
- Exit reasons

Initial backtesting capital:

```text
₹5,000
```

---

# Baseline Backtest Results

The initial strategy without the TP/SL layer produced:

| Metric | Result |
|---|---:|
| Initial Capital | ₹5,000 |
| Final Capital | ₹8,482.51 |
| Total Return | **69.65%** |
| Completed Trades | 252 |
| Winning Trades | 151 |
| Win Rate | 59.92% |
| Gross Profit | ₹6,305.29 |
| Gross Loss | ₹2,822.78 |
| Profit Factor | **2.23** |

### Profit Factor

The baseline strategy achieved:

```text
Profit Factor = 2.23
```

Profit Factor is calculated as:

\[
Profit\ Factor =
\frac{Gross\ Profit}{Gross\ Loss}
\]

A Profit Factor greater than 1 indicates that gross profits exceed gross losses over the tested period.

---

# Risk Management

A configurable risk-management framework was introduced during Phase 6.

The backtesting engine supports:

```text
Stop Loss
Take Profit
Position Reversal
Exit Reason
```

Example configuration:

```python
stop_loss_pct = 1.0
target_pct = 2.0
```

The TP/SL values are configurable and are **not considered final optimized parameters**.

Optimization of these parameters is intentionally reserved for the strategy-optimization phase.

---

# TP/SL Backtest Results

Using a 1% Stop Loss and 2% Take Profit configuration:

| Metric | Result |
|---|---:|
| Initial Capital | ₹5,000 |
| Final Capital | ₹7,589.74 |
| Total Return | **51.79%** |
| Completed Trades | 252 |
| Winning Trades | 147 |
| Win Rate | 58.33% |
| Gross Profit | ₹5,077.74 |
| Gross Loss | ₹2,488.00 |
| Profit Factor | **2.04** |

### Pipeline Integrity Validation

```text
Prediction Count       : 989
Invalid Predictions    : 0
Invalid Trades         : 0
Invalid Quantities     : 0
Invalid P&L             : 0
Capital Check           : PASSED
```

---

# Delta Exchange Integration

The project has now progressed from historical backtesting toward live market-data processing using the **Delta Exchange API**.

Current integration supports retrieval of BTCUSD candle data.

Example:

```python
candles = get_latest_candles(
    symbol="BTCUSD",
    resolution="1h",
    lookback_hours=50
)
```

The API provides:

```text
Open
High
Low
Close
Volume
Timestamp
```

The API timestamps are handled as Unix timestamps in seconds.

---

# Live Feature Engineering

The latest Delta Exchange candles are converted into a Pandas DataFrame and processed using the same feature calculations used during historical development.

Current live pipeline:

```text
Delta Exchange
      │
      ▼
BTCUSD 1H Candles
      │
      ▼
Chronological Sorting
      │
      ▼
Feature Engineering
      │
      ├── RSI
      ├── CCI
      ├── WaveTrend
      ├── +DI
      ├── -DI
      └── ADX
      │
      ▼
Live Feature Vector
```

The live pipeline has successfully generated the following latest feature vector:

```text
RSI       = 42.328312
CCI       = -3.512095
WT1       = -4.788190
WT2       = -12.935420
+DI       = 19.162084
-DI       = 21.159083
ADX       = 32.467179
```

This confirms that the system can successfully transform live Delta Exchange market data into the feature representation required by the Lorentzian classifier.

---

# Current Development Status

## Completed

```text
Phase 1  Project Setup                         ✅
Phase 2  Lorentzian Distance                   ✅
Phase 3  Feature Engineering & Labels          ✅
Phase 4  Lorentzian Classification             ✅
Phase 5  Historical Backtesting                ✅
Phase 6  Strategy Evaluation & TP/SL           ✅
Phase 7  Delta Market Data Integration         🔄
```

### Phase 7 Progress

```text
1. Delta live market-data connection       ✅
2. Latest candle retrieval                 ✅
3. Real-time feature calculation           ✅
4. Live Lorentzian prediction              ⏳
5. Virtual order execution                 ⏳
6. Virtual TP/SL                           ⏳
7. Virtual P&L and trade log               ⏳
8. Continuous paper-trading loop           ⏳
9. Monitoring and safety checks             ⏳
10. Phase 7 validation                      ⏳
```

---

# Roadmap

### Phase 7 — Delta Exchange Virtual / Paper Trading

**Status:** In Progress

#### Completed

- Step 1 — Delta Exchange live market-data connection
- Step 2 — Latest BTCUSD candle retrieval
- Step 3 — Real-time feature calculation
- Step 4 — Live Lorentzian prediction

#### Step 4 — Live Lorentzian Prediction

The system now retrieves the latest BTCUSD candles from Delta Exchange,
calculates the same technical indicators used during historical
classification, and generates a live Lorentzian Classification signal.

Latest feature vector:

| Feature | Value |
|---|---:|
| RSI | 57.508731 |
| CCI | 16.709093 |
| WT1 | 5.662576 |
| WT2 | 2.711408 |
| +DI | 15.332202 |
| -DI | 27.675821 |
| ADX | 28.952983 |

Using `K = 8` nearest neighbours, the live prediction was:

**Prediction: 1 — LONG / BULLISH**

This confirms that the historical Lorentzian classification pipeline
can be connected to live Delta Exchange market data.

#### Remaining Steps

- Step 5 — Virtual order execution
- Step 6 — Virtual TP/SL
- Step 7 — Virtual P&L and trade log
- Step 8 — Continuous paper-trading loop
- Step 9 — Monitoring and safety checks
- Step 10 — Phase 7 validation

The next development stage will connect the live feature pipeline to the Lorentzian classifier.

Planned workflow:

```text
Live BTCUSD Data
       ↓
Feature Calculation
       ↓
Lorentzian Prediction
       ↓
Virtual Order
       ↓
Virtual TP/SL
       ↓
Virtual P&L
       ↓
Trade Log
       ↓
Continuous Paper Trading
```

---

## Phase 8 — Strategy Optimization

Optimization will focus on improving robustness rather than simply maximizing accuracy.

Areas under consideration:

- Number of nearest neighbours (`k`)
- Feature combinations
- Indicator parameters
- Signal filtering
- False-signal reduction
- Stop Loss optimization
- Take Profit optimization
- Position sizing
- Drawdown reduction
- Profit Factor
- Total Return
- Strategy consistency
- Out-of-sample validation

### Primary Evaluation Criteria

```text
Profit Factor
Maximum Drawdown
Total Return
Consistency
Risk-adjusted Performance
```

Win rate will be treated as a supporting metric rather than the primary optimization target.

---

# Phase 9 — Real Trading

Real-money trading will only be considered after successful historical and paper-trading validation.

Planned safeguards include:

- Small initial capital
- Controlled position sizing
- Maximum risk limits
- Real order execution
- Stop Loss protection
- Take Profit management
- Trade monitoring
- Error handling
- Emergency shutdown mechanism

> **Real-money execution is not currently implemented.**

---

# Phase 10 — Final Documentation

The final stage will document:

- System architecture
- Mathematical methodology
- Feature engineering
- Classification methodology
- Backtesting methodology
- Risk management
- Paper-trading results
- Optimization results
- Performance analysis
- Limitations
- Future improvements

---

# Project Structure

```text
lorentzian-classification/
│
├── data/
│   └── raw/
│       └── BTCUSD_1h.csv
│
├── src/
│   ├── data_loader.py
│   ├── lorentzian_classifier.py
│   ├── validation.py
│   ├── backtest_engine.py
│   └── delta_client.py
│
├── tests/
├── __init__.py
├── test_backtest.py
├── test_delta_live.py
├── test_latest_candles.py
├── test_live_features.py
├── test_live_prediction.py
└── test_lorentzian_classifier.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| Market Data | Delta Exchange API |
| Classification | Lorentzian Distance + Nearest Neighbours |
| Backtesting | Custom Python Engine |
| Development | VS Code |
| Environment | Python Virtual Environment |
| Version Control | Git / GitHub |

---

# Design Principles

### Modular Architecture

Each major component is separated into its own module so that data ingestion, feature engineering, classification, backtesting and trading execution can be developed and tested independently.

### Consistent Feature Pipeline

The same feature-engineering logic is reused for historical and live data processing wherever possible.

### Risk-Aware Development

The project evaluates strategies using:

- Profit Factor
- Maximum Drawdown
- Total Return
- Trade consistency
- Capital preservation

rather than relying solely on classification accuracy.

### Validation Before Deployment

The system follows a staged progression:

```text
Historical Data
      ↓
Validation
      ↓
Backtesting
      ↓
Risk Management
      ↓
Paper Trading
      ↓
Optimization
      ↓
Controlled Deployment
```

### No Premature Real Trading

Real-money execution is intentionally separated from the research and paper-trading stages.

---

# Testing Strategy

The project includes dedicated tests for major components.

Examples include:

```text
Feature calculation
Lorentzian distance
Classification
Backtesting
Delta API connectivity
Live candle retrieval
Live feature calculation
```

The goal is to validate individual components before integrating them into the complete trading pipeline.

---

# Key Learnings

This project explores several practical aspects of quantitative and machine-learning-based trading:

- Applying alternative distance metrics to financial time series
- Designing feature vectors for market-state classification
- Building a custom backtesting engine
- Translating predictions into trading positions
- Implementing risk-management logic
- Validating capital and P&L integrity
- Connecting a research system to live market data
- Maintaining consistency between historical and live pipelines
- Separating research, paper trading and real execution
- Evaluating strategies using profitability and risk rather than accuracy alone

---

# Disclaimer

This repository is intended for **educational, research and software-development purposes**.

Historical backtest performance does not guarantee future results.

Cryptocurrency markets are highly volatile and involve substantial financial risk.

Nothing in this repository should be interpreted as financial advice or a recommendation to trade.

The current implementation does **not** execute real-money trades.

This project is being developed incrementally, with each phase validated before moving to the next stage.

---

# Author

**Ram Chandra Murmu**

Data Analytics | Machine Learning | Python | Quantitative Trading Research

This project represents an ongoing exploration of machine learning, quantitative analysis, algorithmic trading and production-oriented Python engineering.

---

## Development Philosophy

> **Build → Validate → Backtest → Manage Risk → Paper Trade → Optimize → Validate Again → Deploy Carefully**

The objective is not simply to produce a profitable backtest, but to build a **transparent, modular, testable and risk-aware trading system** that can be evaluated systematically before any real capital is exposed.
