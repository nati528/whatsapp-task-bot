
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
import os

app = Flask(__name__)  # חשוב שהאפליקציה תוגדר ברמה העליונה

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").strip()
    tasks = load_tasks()
    resp = MessagingResponse()

    if msg.startswith("הוסף משימה:"):
        task_text = msg.replace("הוסף משימה:", "").strip()
        tasks.append({"text": task_text, "done": False})
        save_tasks(tasks)
        resp.message(f"✔️ נוספה משימה: {task_text}")
    elif msg == "רשימת משימות":
        if not tasks:
            resp.message("אין משימות כרגע.")
        else:
            lines = [f"{i+1}. {'[✓]' if t['done'] else '[ ]'} {t['text']}" for i, t in enumerate(tasks)]
            resp.message("\n".join(lines))
    elif msg.startswith("בוצע:"):
        try:
            index = int(msg.replace("בוצע:", "").strip()) - 1
            tasks[index]["done"] = True
            save_tasks(tasks)
            resp.message("✅ עודכן כבוצע.")
        except:
            resp.message("❌ מספר משימה לא תקין.")
    else:
        resp.message("❓ לא זוהתה פקודה. נסה: 'הוסף משימה: ...' או 'רשימת משימות' או 'בוצע: מספר'")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
