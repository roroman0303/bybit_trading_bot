import ccxt
import config  # новый модуль
from utils.timeframes import to_ccxt_tf

class Exchange:
    def __init__(self, cfg):
        options = cfg.get('ccxt', {})
        self.symbol = cfg['symbol']
        self.timeframe = to_ccxt_tf(cfg['timeframe'])
        use_testnet = (config.MODE != "real")
        self.ex = ccxt.bybit({
            "apiKey": config.BYBIT_API_KEY,
            "secret": config.BYBIT_API_SECRET,
            "enableRateLimit": options.get("enableRateLimit", True),
            "options": options.get("options", {"defaultType": "swap"})
        })
        if use_testnet:
            self.ex.set_sandbox_mode(True)
    def fetch_ohlcv(self, limit=500): return self.ex.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=limit)
    def fetch_ticker(self): return self.ex.fetch_ticker(self.symbol)
    def market_buy(self, qty): return self.ex.create_order(self.symbol, type="market", side="buy", amount=qty)
    def market_sell(self, qty): return self.ex.create_order(self.symbol, type="market", side="sell", amount=qty)
