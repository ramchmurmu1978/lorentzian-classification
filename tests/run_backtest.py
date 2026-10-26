from pyexpat import features

import pandas as pd

from src.data_loader import(
    calculate_rsi,
    calculate_cci,
    calculate_wavetrend,
    calculate_adx,
    calculate_label
)
from src.validation import generate_predictions
from src.backtest_engine import BacktestEngine

#-----------------------------------------------#
#   Load historical data and calculate features #
#-----------------------------------------------#

df = pd.read_csv("data/raw/BTCUSD_1h.csv")
df["time"] = pd.to_datetime(df["time"])


#-----------------------------------------------#
#   Calculate predefined features               #
# ----------------------------------------------#

df = calculate_rsi(df)
df = calculate_cci(df)
df = calculate_wavetrend(df)
df = calculate_adx(df)
df = calculate_label(df, horizon=4)


#-----------------------------------------------#
#   Feature Matrix                              #
#-----------------------------------------------#

feature_matrix = df[
    [
        "rsi",
        "cci",
        "wt1",
        "wt2",
        "plus_di",
        "minus_di",
        "adx"
    ]
].copy()

#-----------------------------------------------#
#   Generate Phase 4 predictions                #
#-----------------------------------------------#

predictions, actual_labels = generate_predictions(
    df,
    feature_matrix,
    k=8
)

#-----------------------------------------------#
#   Backtest predictions                        #
#-----------------------------------------------#

engine = BacktestEngine(
    initial_capital=5000,
    stop_loss_pct=1.0,
    target_pct=2.0
)


valid_features = feature_matrix.dropna()
for position, prediction in enumerate(predictions):
    data_index = valid_features.index[position]

    time = df.loc[data_index, "time"]
    price = df.loc[data_index, "close"]
    high = df.loc[data_index, "high"]
    low = df.loc[data_index, "low"]

    # Check TP/SL for the existing position
    if engine.current_trade is not None:
    
        engine.check_take_profit_stop_loss(
        time=time,
        high=high,
        low=low
    )
      
# Process the current classifier signal
    engine.process_signal(
        time=time,
        price=price,
        signal=prediction
    )

#-----------------------------------------------#
#   Pipeline Validation                         #
#-----------------------------------------------#

print("\n----PIPELINE VALIDATION----")

# Prediction counts
print("Prediction Counts: {}".format(len(predictions)))

# Check for invalid predictions
invalid_predictions = [
    prediction for prediction in predictions
    if prediction not in [-1, 1]
]

print("Invalid Predictions: {}".format(len(invalid_predictions)))

# Validate completed trades
 
invalid_trades = 0
invalid_quantities = 0
invalid_pnl = 0

for trade in engine.trades:

    if (
        trade.entry_time is None
        or trade.entry_price <= 0
        or trade.exit_time is None
        or trade.exit_price <= 0
        or trade.direction not in (1,-1)
    ):
        invalid_trades += 1

    if trade.quantity <= 0:
        invalid_quantities += 1

    if trade.profit_loss is None:
        invalid_pnl += 1

print("Invalid Trades: {}".format(invalid_trades))
print("Invalid Quantities: {}".format(invalid_quantities))
print("Invalid P&L: {}".format(invalid_pnl))

# Capital integrity check

total_pnl = sum(
    trade.profit_loss
    for trade in engine.trades
)

expected_capital = engine.initial_capital + total_pnl

if round(engine.capital, 2) == round(expected_capital, 2):
    print("Capital Check: PASSED")
else:
    print("Capital Check: FAILED")
    print("Expected Capital: {}".format(expected_capital))
    print("Actual Capital: {}".format(engine.capital))

#-----------------------------------------------#
#   Backtest results                            #
#-----------------------------------------------#

print("\n----BACKTEST RESULTS----")
print("Initial Capital:", engine.initial_capital)
print("Final Capital:", engine.capital)
print("Completed Trades:", len(engine.trades))

#-----------------------------------------------#
#   Print trade log                             #
#-----------------------------------------------#
"""
print("\n----TRADE LOG----")
for trade_number, trade in enumerate(
        engine.trades,
        start=1
        ):
    print(
        trade_number,
        trade.entry_time,
        trade.entry_price,
        trade.direction,
        trade.quantity,
        trade.exit_time,
        trade.exit_price,
        trade.profit_loss
    )
    print("--------------------")
"""

#----------------------------------------------#
#   Performance Metrics                        #
#----------------------------------------------#

total_return = (
    (engine.capital - engine.initial_capital)
    / engine.initial_capital
) * 100

winning_trades = sum(
    1 for trade in engine.trades
    if trade.profit_loss > 0
)

total_trades = len(engine.trades)

win_rate = (
    winning_trades / total_trades
) * 100

print("\n----PERFORMANCE METRICS----")
print("Total Return: {:.2f}%".format(total_return))
print("Winning Trades: {}".format(winning_trades))
print("Total Trades: {}".format(total_trades))
print("Win Rate: {:.2f}%".format(win_rate))

#----------------------------------------------#
#  Profit Factor                               #
#----------------------------------------------#

gross_profit = sum(
    trade.profit_loss
    for trade in engine.trades
    if trade.profit_loss > 0
)

gross_loss = abs(sum(
    trade.profit_loss
    for trade in engine.trades
    if trade.profit_loss < 0
))

profit_factor = (
    gross_profit / gross_loss
    if gross_loss > 0 else float('inf')
)

print("\n----PROFIT FACTOR----")
print("Gross Profit: {:.2f}".format(gross_profit))
print("Gross Loss: {:.2f}".format(gross_loss))
print("Profit Factor: {:.2f}".format(profit_factor))
