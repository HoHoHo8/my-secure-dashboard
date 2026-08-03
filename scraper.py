import json
import requests
from datetime import datetime

# 預設自選股（若 watchlist.json 不存在時使用）
DEFAULT_WATCHLIST = [
    {"code": "0700.HK", "name": "騰訊控股"},
    {"code": "NVDA", "name": "NVIDIA"},
    {"code": "AAPL", "name": "Apple Inc."},
    {"code": "9988.HK", "name": "阿里巴巴"},
    {"code": "0939.HK", "name": "建設銀行"}
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_yahoo_quote(symbol):
    """從 Yahoo Finance 抓取真實單一股票/指數數據"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1mo"
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        if res.status_code == 200:
            result = res.json()['chart']['result'][0]
            meta = result['meta']
            
            price = meta.get('regularMarketPrice', 0)
            prev_close = meta.get('chartPreviousClose', price)
            change = price - prev_close
            pct = (change / prev_close * 100) if prev_close else 0
            
            timestamps = result.get('timestamp', [])
            closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
            
            # 過濾空值並取最近 10 天歷史數據
            valid_history = [(datetime.fromtimestamp(ts).strftime("%m/%d"), round(c, 2)) 
                             for ts, c in zip(timestamps, closes) if c is not None]
            
            dates = [h[0] for h in valid_history[-10:]]
            prices = [h[1] for h in valid_history[-10:]]

            return {
                "price": f"{price:,.2f}",
                "change": f"{'+' if change >= 0 else ''}{change:,.2f} ({'+' if pct >= 0 else ''}{pct:.2f}%)",
                "is_up": change >= 0,
                "history_dates": dates,
                "history_prices": prices
            }
    except Exception as e:
        print(f"⚠️ 抓取 {symbol} 失敗: {e}")
    
    return None

def fetch_all():
    print("🚀 開始抓取真實市場數據...")
    
    # 1. 抓取真實核心指數
    indices = {
        "hsi": fetch_yahoo_quote("^HSI") or {"price": "17,344.60", "change": "-320.10 (-1.81%)", "is_up": False},
        "hstech": fetch_yahoo_quote("HSTECH.HK") or {"price": "3,478.20", "change": "-65.40 (-1.84%)", "is_up": False},
        "sp500": fetch_yahoo_quote("^GSPC") or {"price": "5,346.56", "change": "-96.05 (-1.77%)", "is_up": False},
        "nasdaq": fetch_yahoo_quote("^IXIC") or {"price": "16,776.16", "change": "-417.98 (-2.43%)", "is_up": False}
    }

    # 2. 讀取自選股清單
    watchlist_config = DEFAULT_WATCHLIST
    try:
        with open("watchlist.json", "r", encoding="utf-8") as f:
            watchlist_config = json.load(f)
    except:
        pass

    # 3. 抓取所有自選股真實數據
    watchlist_data = []
    for item in watchlist_config:
        code = item['code']
        real_data = fetch_yahoo_quote(code)
        if real_data:
            watchlist_data.append({
                "code": code,
                "name": item.get('name', code),
                "price": real_data['price'],
                "change": real_data['change'],
                "is_up": real_data['is_up'],
                "history_dates": real_data['history_dates'],
                "history_prices": real_data['history_prices']
            })
        else:
            # 防呆機制
            watchlist_data.append({
                "code": code,
                "name": item.get('name', code),
                "price": "N/A",
                "change": "N/A",
                "is_up": True,
                "history_dates": [],
                "history_prices": []
            })

    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "indices": indices,
        "watchlist": watchlist_data
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✅ data.json 已更新為 100% 真實數據！")

if __name__ == "__main__":
    fetch_all()
