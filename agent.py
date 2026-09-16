from pathlib import Path
import requests
import os

def ask_online_ai(message):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "API key ونه موندل شو."

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content": message}]
            },
            timeout=15
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"تېروتنه: {e}"

print("Offline Hybrid Agent")
print("امرونه: جوړ کړه، ولیکه، ولوله، پوښتنه، exit")

while True:
    command = input("ته: ").strip()

    if command.lower() in ["exit", "quit", "بند"]:
        print("Agent بند شو.")
        break

    if command.startswith("جوړ کړه "):
        name = command[8:].strip()
        Path(name).write_text("", encoding="utf-8")
        print("فایل جوړ شو:", name)

    elif command.startswith("ولیکه "):
        parts = command[6:].split(" ", 1)
        if len(parts) < 2:
            print("د فایل نوم او متن ولیکه.")
        else:
            name, text = parts
            Path(name).write_text(text, encoding="utf-8")
            print("متن په فایل کې ولیکل شو.")

    elif command.startswith("ولوله "):
        name = command[6:].strip()
        try:
            print(Path(name).read_text(encoding="utf-8"))
        except FileNotFoundError:
            print("فایل پیدا نه شو.")

    elif command.startswith("پوښتنه "):
        msg = command[7:].strip()
        print(ask_online_ai(msg))

    else:
        print("ناپېژندل شوی امر.")
