import requests
import time
import os

WANTED_CODE = os.getenv("VANITY_CODE")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
GUILD_ID = os.getenv("GUILD_ID")

DELAY = float(os.getenv("DELAY_SECONDS", 1.0))

def send_alert():
    vanity_url = f"https://discord.com/channels/{GUILD_ID}/guild-settings/vanity-url"
    
    data = {
        "content": "@everyone ||@here||",
        "embeds": [{
            "title": "⚡ VANITY فاضي!",
            "description": f"**discord.gg/{WANTED_CODE}** صار متوفر الحين!\nروحي خذيه بسرعة.",
            "color": 0x00FF00
        }],
        "components": [{
            "type": 1,
            "components": [{
                "type": 2,
                "style": 5,
                "label": "غيّره الحين",
                "url": vanity_url,
                "emoji": {"name": "🚀"}
            }]
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=data)

def is_code_free(code):
    try:
        r = requests.get(f"https://discord.com/api/v10/invites/{code}", timeout=2.5)
        return r.status_code == 404
    except:
        return False

print(f"جاري مراقبة discord.gg/{WANTED_CODE} ...")
notified = False

while True:
    if is_code_free(WANTED_CODE) and not notified:
        print("⚡ الاختصار فاضي! تم إرسال التنبيه.")
        send_alert()
        notified = True
    elif not is_code_free(WANTED_CODE):
        notified = False
    
    time.sleep(DELAY)