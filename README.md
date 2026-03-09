---
title: 土石流防災即時資訊地圖
emoji: ⚠️
colorFrom: gray
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
---

# 🏔️ 土石流防災即時資訊地圖

一個基於 Gradio + Folium 的互動式災害地點視覺化系統，可部署於 Hugging Face Spaces。

## 功能

- 📍 **互動地圖**：使用 Folium 顯示所有通報地點
- 🚩 **風險等級標記**：紅/橙/綠色圖標表示高/中/低風險
- 📝 **通報提交**：表單輸入新災情，包含地點、描述、坐標、風險等級
- 📋 **通報列表**：即時列出所有通報記錄
- 🤖 **AI 整合**：可擴展 Hugging Face 模型進行圖片辨識或文本分析

## 本地運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 運行
python app.py
```

然後打開瀏覽器訪問 `http://localhost:7860`

## Hugging Face Space 部署

1. 將此專案推送到 GitHub

2. 在 Hugging Face 創建一个新的 Space：
   - 選擇 **Gradio** SDK
   - 名稱如 `dayi-disaster-map`

3. 設定密碼（可選，保護空間）

4. 在 Space 的 Settings → Repository secrets 添加：
   - `HUGGING_FACE_TOKEN`（可選，若需下載私有模型）
   - 其他 API tokens...

5. 將本專案檔案上傳到 Space（或綁定 GitHub repo 自動同步）

6. Space 會自動安裝 `requirements.txt` 並啟動 `app.py`

## 檔案說明

- `app.py` - 主程式，包含 Gradio 介面與 Folium 地圖生成
- `requirements.txt` - Python 套件列表
- `disaster_data.json` - 自動生成的灾害数据存储

## 擴展方向

- 整合 Telegram Bot，自動接收通報
- 使用 Hugging Face 模型自動設定風險等級
- 連接政府開放資料（地質敏感區、雨量站）
- 多使用者支援與權限管理
- 資料庫後端（SQLite / PostgreSQL）
- 郵件/簡訊警示通知

## LICENSE

MIT
