import pandas as pd

def calculate_rsi(df:pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    df["rsi"] = 100 -(100/(1+rs))

    return df

def calculate_cci(df:pd.DataFrame, period: int = 20) -> pd.DataFrame:
    df = df.copy()

    typical_price = (
        df["high"] + df["low"] + df["close"]
    ) / 3

    sma = typical_price.rolling(window=period).mean()

    mean_deviation = typical_price.rolling(window=period).apply(
        lambda x: abs(x - x.mean()).mean(),
        raw=True
    )

    df["cci"] = (
        (typical_price - sma)
        / (0.015 * mean_deviation)
    )

    return df

def calculate_wavetrend(df, channel_length=10, average_length=21):
    """
    Calculate Wavetrend(WT) indicator.
    Parameters:
        df: DataFrame containing high, low and close columns
        channel_length: EMA period for ESA
        average_length: EMA period for WT average
        
        Returns:
            DataFrame with wt1 and wt2 columns 
    """

    # Calculate typical price
    ap = (df["high"] + df["low"] + df["close"]) / 3

    # Exponential moving average of typical price
    esa = ap.ewm(
        span=channel_length,
        adjust=False
    ).mean()

    # Mean deviation
    deviation = (ap - esa).abs().ewm(
        span=channel_length,
        adjust=False
    ).mean()

    # Commodity Index calculation
    ci = (ap - esa) / (0.015 * deviation)

    # Wave Trend main line
    wt1 = ci.ewm(
        span=average_length,
        adjust=False
    ).mean()

    # Wave trend signal line
    wt2 = wt1.rolling(window=4).mean()

    df["wt1"] = wt1
    df["wt2"] = wt2

    return df

def calculate_adx(df, period=14):
    """
    Calculate Average Directional Index (ADX).
    
    Parameters:
        df: DataFrame containing high, low and close columns period: ADX calculation period
        
    Returns:
        DataFrame with +DI, -DI and ADX columns
    """

    high = df["high"]
    low = df["low"]
    close = df["close"]

    # True Range
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    # Directional Movement

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where(
        (up_move > down_move) & (up_move > 0),
        0
    )

    minus_dm = down_move.where(
        (down_move > up_move) & (down_move > 0),
        0
    )

    # Smoothed values
    atr = true_range.ewm(
        alpha=1/period,
        adjust=False
    ).mean()

    plus_dm_smoothed = plus_dm.ewm(
        alpha=1/period,
        adjust=False
    ).mean()

    minus_dm_smoothed = minus_dm.ewm(
        alpha=1/period,
        adjust=False
    ).mean()

    # Directional Indicators:

    plus_di = 100 * (plus_dm_smoothed / atr)
    minus_di = 100 * (minus_dm_smoothed / atr)

    # DX
    dx = (
        100 * (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    )

    # ADX
    adx = dx.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    df["plus_di"] = plus_di
    df["minus_di"] = minus_di
    df["adx"] = adx

    return df

def calculate_label(df, horizon=4):
    """
    Create classification labels based on future price direction.
    Label:
        1 -> future close is higher
       -1 -> future close is lower
        0 -> future close is unchanged
        NaN -> future price is unavailable
    """
    future_close = df["close"].shift(-horizon)

    df["label"] = float("nan")

    df.loc[future_close > df["close"], "label"] = 1
    df.loc[future_close < df["close"], "label"] = -1
    df.loc[future_close == df["close"], "label"] = 0

    return df

def prepare_live_features(candles):
    """
    Convert Delta Exchange candle data into the feature set required by the Lorentzian classifier.

    Args: 
        candles (list): Candle dictionaries returned by API Delta API.
    Returns:
        Dataframe: OHLCV data with calculated features.
    """

    import pandas as pd

    # Convert API response to DataFrame
    df = pd.DataFrame(candles)

    # Convert unix timestamp to datetime
    df["time"] = pd.to_datetime(df["time"], unit="s")

    # Sort chronologically
    df = df.sort_values("time").reset_index(drop=True)

    # Calculate the same features used in Phase 3
    df = calculate_rsi(df)
    df = calculate_cci(df)
    df = calculate_wavetrend(df)
    df = calculate_adx(df)
    
    return df