import os.path
import base64
import requests
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 1. 設定區 ---
# 請將下方的網址換成你的 Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1488569990901796996/HbGE9JQDh4lh-xmAS1PuVnWEGjG7WyiqPRVLrfeXPsktchfdZsaVIFwHCgTmNrsoDEQL"

# 設定 Gmail 存取範圍 (唯讀模式)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def send_to_discord(subject, snippet, sender):
    """將過濾後的郵件資訊發送到 Discord"""
    payload = {
        "username": "Gmail 智慧過濾機器人",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/281/281769.png", # Gmail 圖示
        "embeds": [{
            "title": "📩 發現重要郵件！",
            "color": 15158332, # 紅色
            "fields": [
                {"name": "標題", "value": subject, "inline": False},
                {"name": "寄件者", "value": sender, "inline": False},
                {"name": "摘要", "value": f"{snippet[:100]}...", "inline": False}
            ],
            "footer": {"text": "由 Python 自動偵測推播"}
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print(f"✅ 成功傳送到 Discord: {subject}")
        else:
            print(f"❌ Discord 傳送失敗，狀態碼: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 發送通知時發生錯誤: {e}")

def get_gmail_service():
    """處理 Google OAuth2 登入與授權"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def main():
    print("🚀 啟動 Gmail 智慧過濾系統...")
    service = get_gmail_service()
    
    # 抓取最近的 100 封郵件
    results = service.users().messages().list(userId='me', maxResults=100).execute()
    messages = results.get('messages', [])

    if not messages:
        print('📭 目前收件匣沒有新郵件。')
    else:
        print(f"--- 🔍 正在掃描最新的 {len(messages)} 封郵件 ---")
        
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
            # 解析郵件內容
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "無標題")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "未知寄件者")
            snippet = msg['snippet']

            # 🎯 關鍵字過濾清單 (可根據需求修改)
            keywords = ['元智', 'yzu', '課程', '作業', '老師', '公告', '大學','截止']
            
            # 判斷是否符合關鍵字
            if any(word.lower() in subject.lower() or word.lower() in snippet.lower() for word in keywords):
                print(f"📌 匹配到關鍵字：{subject}")
                # 執行發送到 Discord
                send_to_discord(subject, snippet, sender)
        
        print("--- ✅ 掃描完畢 ---")

if __name__ == '__main__':
    main()