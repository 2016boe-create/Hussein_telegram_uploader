# Hussein Telegram Uploader - Python version (Flask webhook)
# Usage:
# - Set environment variable BOT_TOKEN (do NOT put token here)
# - Start with: gunicorn bot:app --bind 0.0.0.0:$PORT
# - On Render set Start Command to: gunicorn bot:app --bind 0.0.0.0:$PORT

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv('6140362743:AAEDXyA37n0gNnxwnertVcf3ZKe_9mAPVgE')
if not BOT_TOKEN:
    raise RuntimeError("Please set the BOT_TOKEN environment variable.")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
SEEN_FILE = os.path.join(UPLOAD_DIR, 'seen_users.txt')
os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(SEEN_FILE):
    open(SEEN_FILE, 'a').close()

def send_message(chat_id, text):
    requests.get(API_URL + 'sendMessage', params={'chat_id': chat_id, 'text': text})

@app.route('/bot', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return "No update", 200

    message = update.get('message', {})
    chat = message.get('chat', {})
    chat_id = chat.get('id')
    from_user = message.get('from', {})
    from_id = from_user.get('id')

    # welcome message once
    with open(SEEN_FILE, 'r+') as f:
        seen = set(line.strip() for line in f if line.strip())
        if str(from_id) not in seen:
            f.write(str(from_id) + '\n')
            send_message(chat_id, "مرحبًا! أرسل لي أي ملف وسأرفعه لك 🔼")

    document = message.get('document')
    if document:
        file_id = document.get('file_id')
        # get file path
        r = requests.get(API_URL + 'getFile', params={'file_id': file_id})
        j = r.json()
        if not j.get('ok'):
            send_message(chat_id, "❌ فشل الحصول على معلومات الملف.")
            return jsonify({'status':'error'}), 200
        file_path = j['result']['file_path']
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        local_name = os.path.join(UPLOAD_DIR, os.path.basename(file_path))
        dl = requests.get(download_url)
        if dl.status_code == 200:
            with open(local_name, 'wb') as f:
                f.write(dl.content)
            send_message(chat_id, f"✅ تم حفظ الملف في السيرفر: {os.path.basename(local_name)}")
        else:
            send_message(chat_id, "❌ فشل تنزيل الملف.")
    else:
        send_message(chat_id, "أرسل لي ملفًا وسأحفظه لك 📥")

    return jsonify({'status':'ok'}), 200

@app.route('/', methods=['GET'])
def index():
    return "Hussein Telegram Uploader (Python) is running.", 200

if __name__ == '__main__':
    # Local debug
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
