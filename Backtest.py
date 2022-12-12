import pandas as pd
import pandas_ta as ta
import json

class Backtest:
    def __init__(self, initQ, candles, leverage = 2, takeprofit = 0.01, stoploss = 0.01):
        self.buy = False
        self.sell = False
        self.winRate = []
        self.wallet = [initQ]
        self.saveWallet = [0]
        self.initQ = initQ
        self.stoploss = stoploss
        self.takeprofit = takeprofit
        self.leverage = leverage
        self.candles = candles

    def backtest_long(self, strategy):
        self.buy = False
        for i in self.candles.index:
            if strategy(self.candles[i:i+1]) and not self.buy:
                self.buy = self.candles["close"][i]
            elif self.buy and self.candles["close"][i] <= (self.buy - (self.buy * self.stoploss)):
                self.winRate.append(0)
                r = self.wallet[-1] + (self.wallet[-1] * ((self.candles["close"][i] - self.buy)/self.buy) * self.leverage)
                self.wallet.append(r)
                self.buy = False
            elif self.buy and self.candles["close"][i] >= (self.buy + (self.buy * self.takeprofit)):
                self.winRate.append(1)
                if self.wallet[-1] < self.initQ:
                    r = self.wallet[-1] + (self.wallet[-1] * ((self.candles["close"][i] - self.buy)/self.buy) * self.leverage)
                    self.wallet.append(r)
                else:
                    r = self.saveWallet[-1] + (self.wallet[-1] * ((self.candles["close"][i] - self.buy)/self.buy) * self.leverage)
                    self.saveWallet.append(r)
                self.buy = False
        return {
            "win_rate": self.winRate,
            "wallet": self.wallet,
            "saved": self.saveWallet,
        }

    def backtest_short(self, strategy):
        self.buy = False
        for j in range(500, len(self.candles["close"])):
            i = self.candles.index[j]
            if strategy(self.candles[i:i+1]) and not self.buy:
                self.buy = self.candles["close"][i]
            elif self.buy and self.candles["close"][i] >= (self.buy + (self.buy * self.stoploss)):
                self.winRate.append(0)
                r = self.wallet[-1] + (self.wallet[-1] * ((self.buy - self.candles["close"][i])/self.buy) * self.leverage)
                self.wallet.append(r)
                self.buy = False
            elif self.buy and self.candles["close"][i] <= (self.buy - (self.buy * self.takeprofit)):
                self.winRate.append(1)
                if self.wallet[-1] < self.initQ:
                    r = self.wallet[-1] + (self.wallet[-1] * ((self.buy - self.candles["close"][i])/self.buy) * self.leverage)
                    self.wallet.append(r)
                else:
                    r = self.saveWallet[-1] + (self.wallet[-1] * ((self.buy - self.candles["close"][i])/self.buy) * self.leverage)
                    self.saveWallet.append(r)
                self.buy = False
        return {
            "win_rate": self.winRate,
            "wallet": self.wallet,
            "saved": self.saveWallet,
        }
