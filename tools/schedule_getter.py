from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_events():
    """
    今日の予定をGoogleカレンダーから取得します。
    初回実行時は認証が必要です。
    """
    creds = None
    # トークンが保存されている場合は読み込む
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # 有効な認証情報がない場合は、ユーザーにログインを要求
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 認証情報を保存
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # 今日の日付を取得
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # カレンダーイベントを取得
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat() + 'Z',
        timeMax=end_of_day.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return "今日の予定はありません。"

    # 予定を整形
    schedule_text = "今日の予定:\n\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        # 日付と時刻を整形
        if 'T' in start:  # 時刻がある場合
            start_time = datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%H:%M')
            end_time = datetime.fromisoformat(end.replace('Z', '+00:00')).strftime('%H:%M')
            time_str = f"{start_time} - {end_time}"
        else:  # 終日の予定の場合
            time_str = "終日"

        schedule_text += f"・{event['summary']} ({time_str})\n"

    return schedule_text 