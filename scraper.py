import json
import os
import random
import time
from datetime import datetime

# ---------------------------------------------------------
# 🔒 SECURITY CHECKPOINT 1: 安全讀取環境變數 (不將密碼硬編碼在程式中)
# ---------------------------------------------------------
API_KEY = os.getenv("MY_API_SECRET")
if API_KEY:
    print("🔐 安全檢查 passed：已成功加載 GitHub Secrets 憑證！")
else:
    print("ℹ️ 未檢測到 API Key，使用公開爬蟲模式運作。")

# ---------------------------------------------------------
# 🔒 SECURITY CHECKPOINT 2: 禮貌爬蟲延遲 (防止對目標網站造成負擔或被封鎖)
# ---------------------------------------------------------
print("⏳ 啟動禮貌延遲，模擬正常人行為...")
time.sleep(random.uniform(1.0, 3.0))

# ---------------------------------------------------------
# 數據採集與分析邏輯 (此處為範例數據生成，可改為實際爬蟲)
# ---------------------------------------------------------
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 🔒 SECURITY CHECKPOINT 3: 只輸出去識別化的聚合數據 (Aggregated Data)
# 嚴禁在 data.json 包含個人敏感資訊 (PII)
dashboard_data = {
    "last_updated": now,
    "total_count": random.randint(12000, 18000),
    "today_count": random.randint(800, 2500),
    "rate": f"{round(random.uniform(6.5, 14.0), 1)}%",
    "trend_labels": ["週一", "週二", "週三", "週四", "週五", "週六", "週日"],
    "trend_values": [random.randint(1500, 4500) for _ in range(7)],
    "bar_labels": ["類別 A", "類別 B", "類別 C", "類別 D"],
    "bar_values": [random.randint(300, 1800) for _ in range(4)]
}

# 寫入公開的 JSON 數據檔
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

print(f"✅ [{now}] 數據已安全清洗並寫入 data.json！")
