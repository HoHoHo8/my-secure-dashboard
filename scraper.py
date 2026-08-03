import json
import os
import random
from datetime import datetime

# 嘗試載入 yfinance
try:
    import yfinance as ticker_api
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

def fetch_symbol(symbol, default_price, default_pct):
    """安全抓取個股數據，若失敗自動使用備援數據，防止程式崩潰"""
    if not HAS_YFINANCE:
        return {"price": default_price, "change_pct": default_pct}
    
    try:
        t = ticker_api.Ticker(symbol)
        hist = t.history(period="5d")
        if not hist.empty and len(hist) >= 2:
            current_price = round(float(hist['Close'].iloc[-1]), 2)
            prev_price = round(float(hist['Close'].iloc[-2]), 2)
            change = current_price - prev_price
            change_pct = round((change / prev_price) * 100, 2)
            return {"price": current_price, "change_pct": change_pct}
    except Exception as e:
        print(f"⚠️ 抓取 {symbol} 失敗，啟動備援數據: {e}")
    
    return {"price": default_price, "change_pct": default_pct}

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 開始抓取港美股數據...")

    # 抓取指數
    hsi = fetch_symbol("^HSI", 17532.40, +1.25)
    sp500 = fetch_symbol("^GSPC", 5458.10, +0.85)
    nasdaq = fetch_symbol("^IXIC", 17120.30, -0.42)

    # 港股焦點
    tencent = fetch_symbol("0700.HK", 376.40, +1.82)
    baba = fetch_symbol("9988.HK", 78.90, -0.51)
    meituan = fetch_symbol("3690.HK", 116.50, +2.38)
    xiaomi = fetch_symbol("1810.HK", 16.82, +3.08)

    # 美股焦點
    nvda = fetch_symbol("NVDA", 128.35, +4.21)
    tsla = fetch_symbol("TSLA", 212.50, -2.15)
    aapl = fetch_symbol("AAPL", 224.20, +0.92)
    msft = fetch_symbol("MSFT", 448.90, +1.10)

    # 封裝標準 JSON
    dashboard_data = {
        "last_updated": now,
        "market_sentiment": round(random.uniform(62.0, 75.0), 1),
        "indices": {
            "hsi": hsi,
            "sp500": sp500,
            "nasdaq": nasdaq
        },
        "hk_stocks": [
            {"name": "騰訊控股 (0700.HK)", "price": tencent["price"], "pct": tencent["change_pct"]},
            {"name": "阿里巴巴 (9988.HK)", "price": baba["price"], "pct": baba["change_pct"]},
            {"name": "美團點評 (3690.HK)", "price": meituan["price"], "pct": meituan["change_pct"]},
            {"name": "小米集團 (1810.HK)", "price": xiaomi["price"], "pct": xiaomi["change_pct"]}
        ],
        "us_stocks": [
            {"name": "NVIDIA (NVDA)", "price": nvda["price"], "pct": nvda["change_pct"]},
            {"name": "Tesla (TSLA)", "price": tsla["price"], "pct": tsla["change_pct"]},
            {"name": "Apple (AAPL)", "price": aapl["price"], "pct": aapl["change_pct"]},
            {"name": "Microsoft (MSFT)", "price": msft["price"], "pct": msft["change_pct"]}
        ],
        "trend_labels": ["09:30", "10:30", "11:30", "13:30", "14:30", "15:30", "16:00"],
        "hsi_trend": [17400, 17450, 17420, 17480, 17510, 17490, 17532],
        "us_trend": [17000, 17050, 17020, 17090, 17120, 17080, 17120]
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

    print("✅ data.json 成功更新完畢！")

if __name__ == "__main__":
    main()
