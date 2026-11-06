from datetime import datetime
from src.virtual_executor import VirtualExecutor

def get_time():
    return datetime(2026, 11, 6, 10, 0, 0)

def test_virtual_long_execution():
    executor = VirtualExecutor(initial_capital=5000)

    executor.execute_signal(
        time=get_time(),
        price=100,
        signal=1
    )

    trade = executor.current_trade

    assert trade is not None, "Trade should be initiated"
    assert trade.direction == 1, "Trade direction should be long"
    assert trade.entry_price == 100, "Entry price should be 100"
    assert trade.quantity == 50, "Quantity should be 50"
    assert executor.capital == 5000, "Capital should be 5000"

def test_virtual_short_execution():
    executor = VirtualExecutor(initial_capital=5000)

    executor.execute_signal(
        time=get_time(),
        price=100,
        signal=-1
    )

    trade = executor.current_trade

    assert trade is not None, "Trade should be initiated"
    assert trade.direction == -1, "Trade direction should be short"
    assert trade.entry_price == 100, "Entry price should be 100"
    assert trade.quantity == 50, "Quantity should be 50"
    assert executor.capital == 5000, "Capital should be 5000"

def test_long_to_short_reversal():
    executor = VirtualExecutor(initial_capital=5000)

    executor.execute_signal(get_time(), price=100, signal=1)  # Long
    executor.execute_signal(get_time(), price=90, signal=-1)  # Short

    assert len(executor.trades) == 1, "There should be one completed trade"
    closed_trade = executor.trades[0] 

    assert closed_trade.direction == 1, "Closed trade should be long"
    assert closed_trade.exit_price == 90, "Exit price should be 90"
    assert closed_trade.profit_loss == -500, "Profit/loss should be -500"
    assert closed_trade.exit_reason == "SIGNAL_REVERSAL", "Exit reason should be 'Reversal'"

    assert executor.current_trade is not None, "There should be a new current trade"
    assert executor.current_trade.direction == -1, "Current trade should be short"
    assert executor.current_trade.entry_price == 90, "Entry price of new trade should be 90"

def test_short_to_long_reversal():
    executor = VirtualExecutor(initial_capital=5000)

    executor.execute_signal(get_time(), price=100, signal=-1)  # Short
    executor.execute_signal(get_time(), price=100, signal=1)  # Long

    assert len(executor.trades) == 1, "There should be one completed trade"
    closed_trade = executor.trades[0]

    assert closed_trade.direction == -1, "Closed trade should be short"
    assert closed_trade.exit_price == 100, "Exit price should be 100"
    assert closed_trade.exit_reason == "SIGNAL_REVERSAL", "Exit reason should be 'Reversal'"

    assert executor.current_trade is not None, "There should be a new current trade"
    assert executor.current_trade.direction == 1, "Current trade should be long"
    assert executor.current_trade.entry_price == 100, "Entry price of new trade should be 100"

def test_duplicate_signal_does_not_create_new_position():
    executor = VirtualExecutor(initial_capital=5000)

    executor.execute_signal(get_time(), price=100, signal=1)  # Long
    executor.execute_signal(get_time(), price=100, signal=1)  # Duplicate Long
    original_trade = executor.current_trade

    executor.execute_signal(get_time(), 105, signal=1)  # Another Duplicate Long
    
    assert executor.current_trade is original_trade
    assert executor.current_trade.entry_price == 100, "Entry price should be 100"
    assert len(executor.trades) == 0, "There should be no completed trades"
    assert executor.capital == 5000, "Capital should remain unchanged"
