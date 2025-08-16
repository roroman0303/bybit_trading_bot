import argparse
import csv
import os
import requests
from datetime import datetime

BASE_URL = "https://api.bybit.com/v5/market/kline"

def fetch_klines(symbol: str, interval: str, start: int, end: int, limit: int = 1000):
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
        "limit": limit,
    }
    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    if "result" not in data or "list" not in data["result"]:
        return []
    return data["result"]["list"]

def parse_date(date_str: str) -> int:
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp() * 1000)

def save_to_csv(data, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for row in data:
            ts = int(row[0])
            open_, high, low, close, volume = row[1:6]
            writer.writerow([ts, open_, high, low, close, volume])

def main():
    parser = argparse.ArgumentParser(description="Загрузка исторических данных с Bybit")
    parser.add_argument("--symbol", required=True, help="Торговая пара, например BTCUSDT")
    parser.add_argument("--timeframe", required=True, help="Таймфрейм (1,3,5,15,30,60,240,D,M,W)")
    parser.add_argument("--start", required=True, help="Начальная дата в формате YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Конечная дата в формате YYYY-MM-DD")
    parser.add_argument("--output", required=True, help="Путь для сохранения CSV")
    args = parser.parse_args()

    start_ts = parse_date(args.start)
    end_ts = parse_date(args.end)

    all_candles = []
    chunk = 1000

    print(f"📥 Загружаем {args.symbol} {args.timeframe} с {args.start} по {args.end}...")

    current = start_ts
    while current < end_ts:
        candles = fetch_klines(args.symbol, args.timeframe, current, end_ts, limit=chunk)
        if not candles:
            break
        candles_sorted = sorted(candles, key=lambda x: int(x[0]))
        all_candles.extend(candles_sorted)
        last_ts = int(candles_sorted[-1][0])
        current = last_ts + 1
        print(f"Загружено {len(all_candles)} свечей...")

    save_to_csv(all_candles, args.output)
    print(f"✅ Данные сохранены в {args.output}, всего {len(all_candles)} свечей")

if __name__ == "__main__":
    main()
