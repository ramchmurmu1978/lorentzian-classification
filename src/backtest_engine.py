from dataclasses import dataclass

@dataclass
class Trade:
    """Represents a trade executed during backtesting."""
    entry_time: object
    entry_price: float
    direction: int  # 1 for long, -1 for short
    quantity: float = 0.0

    stop_loss: float = None
    take_profit: float = None

    exit_time: object = None
    exit_price: float = None
    profit_loss: float = 0.0
    exit_reason: str = None  # e.g., 'stop_loss', 'take_profit', 'signal'

class BacktestEngine:
    """Backtest engine for evaluating trading strategies."""

    def __init__(self,initial_capital=5000, stop_loss_pct=None, target_pct=None):

        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.stop_loss_pct = stop_loss_pct
        self.target_pct = target_pct
        self.trades = []
        self.current_trade = None

    def reset(self):
        self.capital = self.initial_capital
        self.trades = []
        self.current_trade = None

    def open_position(self, time, price, direction):
        """Open a long or short position.
        
        direction:
            1 for long, -1 for short
        """
        quantity = self.capital / price

        stop_loss = None
        take_profit = None

        if self.current_trade is not None:
            raise ValueError("A trade is already open.")

        if self.stop_loss_pct is not None:
            if direction == 1:  # Long
                stop_loss = price * (1 - self.stop_loss_pct/100)
            else:  # Short
                stop_loss = price * (1 + self.stop_loss_pct/100)

        if self.target_pct is not None:
            if direction == 1:  # Long
                take_profit = price * (1 + self.target_pct/100)
            else:  # Short
                take_profit = price * (1 - self.target_pct/100)

        self.current_trade = Trade(
            entry_time=time,
            entry_price=price,
            direction=direction,
            quantity=quantity
        )

    def close_position(self, time, price, reason=None):
        """
        Close the currently open position and calculate profit/loss.
        """

        if self.current_trade is None:  
            return  # No trade to close
        trade = self.current_trade

        trade.exit_time = time
        trade.exit_price = price
        trade.exit_reason = reason

        if trade.direction == 1:
            profit_loss = (
                price - trade.entry_price
            ) * trade.quantity

        else:
            profit_loss = (
                trade.entry_price - price
            ) * trade.quantity

        trade.exit_time = time
        trade.exit_price = price
        trade.profit_loss = profit_loss

        self.capital += profit_loss
        self.trades.append(trade)
        self.current_trade = None

    def check_take_profit_stop_loss(self, time, high, low):

        if self.current_trade is None:
            return False  # No trade to check
        trade = self.current_trade

        # Long position
        if trade.direction == 1:
            stop_hit = (
                trade.stop_loss is not None
                and low <= trade.stop_loss
            )

            target_hit = (
                trade.take_profit is not None
                and high >= trade.take_profit
            )

            # Conservative assumption:
            # If both are hit in the same candle assume Stop Loss happened first.
            if stop_hit:
                self.close_position(
                    time,
                    trade.stop_loss,
                    reason="STOP_LOSS"
                )
                return True
            
            if target_hit:
                self.close_position(
                    time,
                    trade.take_profit,
                    reason="TAKE_PROFIT"
                )
                return True
        
        # Short Position
        elif trade.direction == -1:

            stop_hit = (
                trade.stop_loss is not None
                and high >= trade.stop_loss
            )
            target_hit = (
                trade.take_profit is not None
                and low <= trade.take_profit
            )

        # Conservative assumption:
        # If both are hit in the same candle, assume Stop Loss happened first.

        if stop_hit:
            self.close_position(
                time,
                trade.stop_loss,
                reason="STOP_LOSS"
            )
            return True
        if target_hit:
            self.close_position(
                time,
                trade.take_profit,
                reason="TAKE_PROFIT"
            )
            return True
        return False


    def process_signal(self, time, price, signal):
        """
        Process a trading signal.
        
        signal:
            1 for long, -1 for short, 0 for no action
        """
        if signal not in (1, -1):
            return  # No action for signal 0

        # No open position
        if self.current_trade is None:
            self.open_position(
                time,
                price,
                signal
            )
            return

        # Same direction -> hold position
        if self.current_trade.direction == signal:
            return  # Hold position

        # Opposite signal -> close current position and open new one
        self.close_position(
            time,
            price,
            reason="STRONG_REVARSAL"
        )

        # Open new position in the opposite direction
        self.open_position(
            time,
            price,
            signal
        )