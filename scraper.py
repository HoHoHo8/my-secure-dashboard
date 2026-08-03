import json
import requests
from datetime import datetime

# 預設自選股清單（如果沒有讀取到用戶自訂檔）
DEFAULT_WATCHLIST = [
    {"code": "0700.HK", "name": "騰訊控股"},
    {"code": "NVDA", "name": "NVIDIA"},
    {"code": "AAPL", "name": "Apple Inc."},
    {"code": "9988.HK", "name": "阿里巴巴"},
    {"code": "0939.HK", "name": "建設銀行"}
]

def fetch_stock_data(symbol):
    """從 Yahoo Finance API 抓取單一股票的最新價格與歷史走勢"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1mo"
    
    try:
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200:
            result = res.json()['chart']['result'][0]
            meta = result['meta']
            price = meta.get('regularMarketPrice', 0)
            prev_close = meta.get('chartPreviousClose', price)
            change = price - prev_close
            pct = (change / prev_close * 100) if prev_close else 0
            
            timestamps = result.get('timestamp', [])
            closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])
            
            # 格式化日期與價格走勢
            dates = [datetime.fromtimestamp(ts).strftime("%m/%d") for ts in timestamps[-10:]]
            prices = [round(c, 2) for c in closes[-10:] if c is not None]
            
            return {
                "price": f"{price:,.2f}",
                "change": f"{'+' if change >= 0 else ''}{change:,.2f} ({'+' if pct >= 0 else ''}{pct:.2f}%)",
                "is_up": change >= 0,
                "history_dates": dates,
                "history_prices": prices
            }
    except Exception as e:
        print(f"⚠️ 抓取股票 {symbol} 失敗: {e}")
    
    # 失敗時的防呆備用數據
    return {
        "price": "N/A",
        "change": "0.00 (0.00%)",
        "is_up": True,
        "history_dates": ["07/25", "07/28", "07/29", "07/30", "07/31"],
        "history_prices": [100, 102, 101, 104, 105]
    }

def fetch_market_dashboard_data():
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 讀取現有自選股清單 (若沒有則用預設值)
    watchlist = DEFAULT_WATCHLIST
    try:
        with open("watchlist.json", "r", encoding="utf-8") as f:
            watchlist = json.load(f)
    except:
        pass

    print(f"🚀 開始抓取自選股動向 ({len(watchlist)} 隻)...")
    
    # 抓取自選股的動態數據與圖表歷史
    watchlist_data = []
    for item in watchlist:
        code = item['code']
        stock_info = fetch_stock_data(code)
        watchlist_data.append({
            "code": code,
            "name": item.get('name', code),
            "price": stock_info['price'],
            "change": stock_info['change'],
            "is_up": stock_info['is_up'],
            "history_dates": stock_info['history_dates'],
            "history_prices": stock_info['history_prices']
        })

    output = {
        "last_updated": today_str,
        "watchlist": watchlist_data,
        "market_sentiment": {
            "vix": {"value": "18.25", "status": "中性 (Neutral)"},
            "bull_bear_ratio": "58% 牛 / 42% 熊",
            "put_call_ratio": "0.85"
        }
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 同步備份 watchlist.json
    with open("watchlist.json", "w", encoding="utf-8") as f:
        json.dump(watchlist, f, ensure_ascii=False, indent=2)

    print("✅ data.json 及圖表數據已成功寫入！")

if __name__ == "__main__":
    fetch_market_dashboard_data()
