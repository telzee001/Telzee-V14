
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np

class TelzeeV14(IStrategy):
    INTERFACE_VERSION = 3
    leverage = 20
    base_risk_pct = 10.0
    safety_risk_pct = 2.0
    tp_multiplier = 2.5
    atr_length = 14
    minimal_roi = {"0": 100}
    stoploss = -1.0
    trailing_stop = True
    timeframe = '15m'
    process_only_new_candles = True
    use_exit_signal = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema4h'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['ema1h'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['vwap'] = qtpylib.vwap(dataframe)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['vol_ma'] = ta.SMA(dataframe['volume'], timeperiod=20)
        dataframe['vol_spike'] = dataframe['volume'] > (dataframe['vol_ma'] * 1.3)
        dataframe['upper_fractal'] = dataframe['high'].rolling(window=5).max().shift(1)
        dataframe['lower_fractal'] = dataframe['low'].rolling(window=5).min().shift(1)
        dataframe['momentum_ok'] = dataframe['close'] > dataframe['close'].shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=self.atr_length)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe['close'] > dataframe['ema4h']) & (dataframe['close'] > dataframe['ema1h']) & (dataframe['close'] > dataframe['vwap']) & (dataframe['close'] > dataframe['upper_fractal']) & (dataframe['rsi'] < 68) & (dataframe['adx'] > 25) & (dataframe['vol_spike']) & (dataframe['momentum_ok']), 'enter_long'] = 1
        dataframe.loc[(dataframe['close'] < dataframe['ema4h']) & (dataframe['close'] < dataframe['ema1h']) & (dataframe['close'] < dataframe['vwap']) & (dataframe['close'] < dataframe['lower_fractal']) & (dataframe['rsi'] > 32) & (dataframe['adx'] > 25) & (dataframe['vol_spike']) & (dataframe['momentum_ok']), 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def leverage(self, *args, **kwargs) -> float:
        return float(self.leverage)
