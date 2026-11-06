from src.backtest_engine import BacktestEngine

class VirtualExecutor:
    """
    Handles virtual/paper order execution. No real orders are sent to Delta Exchange.
    """

    def __init__(
            self,
            initial_capital = 5000,
            stop_loss_pct = None,
            target_pct = None
        ):
            self.engine = BacktestEngine(
                  initial_capital=initial_capital,
                  stop_loss_pct=stop_loss_pct,
                  target_pct=target_pct
            )

    def execute_signal(self, time, price, signal):
          """
          Execute a trading signal virtually.
          signal:
            1   --> LONG
           -1   --> SHORT
            0   --> no action
          """

          self.engine.process_signal(
                time=time,
                price=price,
                signal=signal
          )

    def check_tp_sl(self, time, high, low):
          """
          check whether the current virtual position has reached it's stop loss or take profit.
          """
          return self.engine.check_take_profit_stop_loss(
                time=time,
                high=high,
                low=low
          )

    @property
    def current_trade(self):
          """Return the currently open virtual trade."""
          return self.engine.current_trade
    
    @property
    def trades(self):
          """Return completed virtual trades."""
          return self.engine.trades

    @property
    def capital(self):
          """Return current virtual capital."""
          return self.engine.capital