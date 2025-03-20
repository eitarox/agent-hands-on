from openai import OpenAI
import json
from tools import send_email, get_calendar_events
import os
from dotenv import load_dotenv

def main():
    # 環境変数の読み込み
    load_dotenv()
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    if not recipient_email:
        raise ValueError("RECIPIENT_EMAIL environment variable is not set")

    client = OpenAI()

    tools = [{
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a given recipient with a subject and message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "The recipient email address."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line."
                    },
                    "body": {
                        "type": "string",
                        "description": "Body of the email message."
                    }
                },
                "required": [
                    "to",
                    "subject",
                    "body"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }]

    # カレンダー予定を取得
    schedule = get_calendar_events()
    
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user", 
            "content": f"Can you send an email to {recipient_email} with today's schedule? Here's the schedule:\n\n{schedule}"
        }],
        tools=tools
    )

    # ツールコールの結果を表示
    print("ツールコールの内容:")
    print(completion.choices[0].message.tool_calls)
    print("\nメール送信の実行:")

    # ツールコールの結果を取得
    tool_calls = completion.choices[0].message.tool_calls
    for tool_call in tool_calls:
        if tool_call.function.name == "send_email":
            # JSON文字列をパース
            arguments = json.loads(tool_call.function.arguments)
            # メール送信関数を呼び出し
            send_email(
                to=arguments["to"],
                subject=arguments["subject"],
                body=arguments["body"]
            )

if __name__ == "__main__":
    main()
