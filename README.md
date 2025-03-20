# カレンダー予定メール送信ツール

Google カレンダーから今日の予定を取得し、指定されたメールアドレスに送信するツールです。

## セットアップ手順

1. 必要なパッケージのインストール:

```bash
uv pip install -r requirements.txt
```

2. 環境変数の設定:

- `.env.example`を`.env`にコピーし、以下の情報を設定してください：
  - `EMAIL_USER`: Gmail アドレス
  - `EMAIL_PASSWORD`: Gmail アプリパスワード
  - `OPENAI_API_KEY`: OpenAI API キー

3. Google Calendar API の設定:

- [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
- Google Calendar API を有効化
- 認証情報を作成し、`credentials.json`としてダウンロード
- プロジェクトのルートディレクトリに`credentials.json`を配置

## 使用方法

```bash
uv run main.py
```

初回実行時は、ブラウザが開いて Google アカウントでの認証が求められます。

## 注意事項

- `.env`、`credentials.json`、`token.pickle`は機密情報を含むため、Git にコミットしないでください
- Gmail アプリパスワードは、Google アカウントの設定から生成できます
