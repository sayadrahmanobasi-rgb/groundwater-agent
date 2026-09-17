from pathlib import Path
import requests
import os
import subprocess

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

def git_sync():
    try:
        subprocess.run(["git", "add", "."], check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "Agent خودکار sync"],
            capture_output=True, text=True
        )
        if "nothing to commit" in result.stdout:
            return "هېڅ نوی بدلون نشته."
        return "بدلونونه خوندي شول (Git commit ترسره شو)."
    except Exception as e:
        return f"تېروتنه: {e}"

def get_water_data(lat, lon):
    try:
        url = (
            "https://power.larc.nasa.gov/api/temporal/climatology/point"
            f"?parameters=PRECTOTCORR&community=AG&longitude={lon}&latitude={lat}&format=JSON"
        )
        response = requests.get(url, timeout=15)
        data = response.json()
        rain = data["properties"]["parameter"]["PRECTOTCORR"]
        annual = rain["ANN"]

        if annual >= 2.5:
            level = "لوړ احتمال"
        elif annual >= 1.2:
            level = "منځنی احتمال"
        else:
            level = "ټیټ احتمال"

        result = f"د دې ځای اوسط کلنی باران: {annual} mm/ورځ\n"
        result += f"د اوبو موندلو عمومي احتمال: {level}\n"
        result += "میاشتنی باران (mm/ورځ):\n"
        for month in ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]:
            result += f"  {month}: {rain[month]}\n"
        return result
    except Exception as e:
        return f"تېروتنه: {e}"

print("Offline Hybrid Agent")
print("امرونه: جوړ کړه، ولیکه، ولوله، پوښتنه، sync، اوبه، exit")

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

    elif command.lower() == "sync":
        print(git_sync())

    elif command.startswith("اوبه "):
        parts = command[5:].strip().split(" ")
        if len(parts) < 2:
            print("فورمېټ: اوبه <latitude> <longitude>")
        else:
            try:
                lat, lon = parts[0], parts[1]
                print(get_water_data(lat, lon))
            except Exception as e:
                print(f"تېروتنه: {e}")

    else:
        print("ناپېژندل شوی امر.")
