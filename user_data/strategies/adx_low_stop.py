# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta


# --------------------------------


class adx_low_stop(IStrategy):
    """
    author@: Gert Wohlgemuth
    converted from:
        https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/AdxMomentum.cs
    """

    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    

    # Optimal stoploss designed for the strategy
    

    # Trailing stoploss
    

    # Optimal ticker interval for the strategy
    ticker_interval = '1m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['adx'] > 47) &
                    (dataframe['mom'] < 20) &
                    # (dataframe['minus_di'] > 45) &
                    (dataframe['plus_di'] < dataframe['minus_di'])

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['adx'] > 47) &
                    (dataframe['mom'] > 20) &
                    # (dataframe['minus_di'] > 45) &
                    (dataframe['plus_di'] > dataframe['minus_di'])

            ),
            'sell'] = 1
        return dataframe