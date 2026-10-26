from src.backtest_engine import BacktestEngine

engine = BacktestEngine(initial_capital=5000)

# Open a long position.
engine.process_signal(
    time = "2025-01-01 10:00:00",
    price = 100,
    signal = 1
)

# Reverse to short
engine.process_signal(
    time = "2025-01-01 11:00:00",
    price = 110,
    signal = -1
)

# Close short
engine.process_signal(
    time = "2025-01-01 12:00:00",
    price = 100,
    signal = 1
)

# Display results
print("\n--- Backtest Engine Test ---")

print("Initial Capital:", engine.initial_capital)
print("Final Capital:", engine.capital)
print("Completed Trades:", len(engine.trades))

for trade in engine.trades:
    print("\nTrade:")
    print("Entry Time:", trade.entry_time)
    print("Entry Price:", trade.entry_price)
    print("Direction:", trade.direction)
    print("Quantity:", trade.quantity)
    print("Exit Time:", trade.exit_time)
    print("Exit Price:", trade.exit_price)
    print("Profit/Loss:", trade.profit_loss)