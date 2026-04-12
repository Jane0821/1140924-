# 📧 Gmail 關鍵字偵測與 Discord 自動化提醒工具

這是一個基於 Python 開發的自動化工具，旨在即時監控 Gmail 收件匣，並在收到含有特定關鍵字（如「元智」、「課程」、「作業」）的郵件時，自動發送通知至 Discord 頻道。

## 🌟 主要功能
* **即時監控**：利用 Google Gmail API 持續追蹤最新郵件。
* **關鍵字過濾**：可自定義關鍵字清單，精確篩選重要訊息。
* **Discord 整合**：透過 Webhook 實現即時推送訊息，包含郵件標題、寄件者及簡介。
* **資安防護**：使用 `.gitignore` 確保 API 金鑰與憑證（Credentials）不外流。

## 🛠️ 技術棧
* **語言**：Python 3.x
* **API 使用**：Gmail API, Discord Webhook
* **版本控制**：Git / GitHub

## 📂 檔案結構
* `gmail_bot.py`: 機器人主程式
* `.gitignore`: 設定排除上傳的敏感檔案
* `.venv/`: 虛擬環境配置

## 🚀 執行與部署
1. 安裝需求環境：`pip install google-api-python-client google-auth-oauthlib requests`
2. 放入 `credentials.json`
3. 執行程式：`python gmail_bot.py`
