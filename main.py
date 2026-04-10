from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html dir="rtl">
    <head>
        <title>Builder+ | כניסה</title>
        <style>
            body { font-family: system-ui; background: linear-gradient(135deg, #1e3a8a, #3b82f6); display: flex; justify-content: center; padding-top: 100px; height: 100vh; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 350px; text-align: center; }
            h1 { color: #1e3a8a; font-size: 32px; margin-bottom: 10px; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 2px solid #eee; border-radius: 10px; box-sizing: border-box; font-size: 16px; }
            .btn-login { background: #3b82f6; color: white; border: none; width: 100%; padding: 12px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; margin-top: 10px; }
            .btn-google { background: white; border: 1px solid #ddd; width: 100%; padding: 12px; border-radius: 10px; margin-top: 15px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Builder+</h1>
            <p style="color: #666;">התחברות למערכת המאובטחת</p>
            <input type="email" id="email" placeholder="כתובת אימייל">
            <input type="password" id="key" placeholder="קוד סודי">
            <button class="btn-login" onclick="login()">כניסה</button>
            <button class="btn-google" onclick="alert('התחברות עם גוגל תהיה זמינה בגרסת הענן')">
                <img src="https://google.com" width="16"> כניסה עם Google
            </button>
        </div>
        <script>
            function login() {
                const email = document.getElementById('email').value;
                const key = document.getElementById('key').value;
                if (!email.includes('@')) {
                    alert('נא להזין אימייל תקין');
                } else {
                    window.location.href = '/verify?email=' + email + '&key=' + key;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/verify")
def verify(email: str, key: str):
    if key == "12345":
        return {"status": "success", "user": email, "message": "ברוך הבא למערכת Builder+!"}
    return {"status": "error", "message": "המפתח שהזנת אינו תקין"}
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()
DB_FILE = "users.json"

# פונקציה לטעינת משתמשים מהקובץ
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# פונקציה לשמירת משתמש חדש
def save_user(email, key):
    users = load_users()
    users[email] = key
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html dir="rtl">
    <head>
        <title>Builder+ | כניסה והרשמה</title>
        <style>
            body { font-family: sans-serif; background: #1e3a8a; display: flex; justify-content: center; padding-top: 50px; color: white; }
            .card { background: white; padding: 30px; border-radius: 15px; color: #333; width: 350px; text-align: center; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; }
            .btn { width: 100%; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-bottom: 10px; }
            .btn-login { background: #3b82f6; color: white; }
            .btn-reg { background: #10b981; color: white; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Builder+</h1>
            <p>הכנס מייל ומפתח (או הירשם כמשתמש חדש)</p>
            <input type="email" id="email" placeholder="אימייל">
            <input type="text" id="key" placeholder="מפתח סודי">
            <button class="btn btn-login" onclick="action('login')">כניסה למערכת</button>
            <button class="btn btn-reg" onclick="action('register')">הרשמה וקבלת מפתח</button>
        </div>
        <script>
            function action(type) {
                const email = document.getElementById('email').value;
                const key = document.getElementById('key').value;
                if (!email || !key) return alert('נא למלא מייל ומפתח');
                window.location.href = `/${type}?email=${email}&key=${key}`;
            }
        </script>
    </body>
    </html>
    """

@app.get("/register")
def register(email: str, key: str):
    users = load_users()
    if email in users:
        return {"status": "error", "message": "המשתמש כבר קיים!"}
    save_user(email, key)
    return {"status": "success", "message": f"נרשמת בהצלחה! המפתח שלך הוא: {key}"}

@app.get("/login")
def login(email: str, key: str):
    users = load_users()
    if email in users and users[email] == key:
        return {"status": "success", "message": f"ברוך הבא, {email}!"}
    return {"status": "error", "message": "המייל או המפתח לא תקינים"}
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# בסיס נתונים דמיוני שמראה מה המפתח הזה פותח
services_data = {
    "12345": {
        "name": "אלכס",
        "balance": "₪2,500",
        "email": "alex@gmail.com",
        "notifications": 3,
        "api_access": "Full Access"
    }
}

@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <html dir="rtl">
    <head>
        <title>Builder+ Master Key</title>
        <style>
            body { font-family: 'Segoe UI'; background: #0f172a; display: flex; justify-content: center; padding-top: 100px; color: white; }
            .login-card { background: #1e293b; padding: 40px; border-radius: 20px; width: 350px; text-align: center; border: 1px solid #334155; }
            h1 { color: #38bdf8; }
            input { width: 100%; padding: 12px; margin: 20px 0; border-radius: 10px; border: none; background: #334155; color: white; }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px; border: none; width: 100%; border-radius: 10px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h1>Builder+</h1>
            <p>הזן את המפתח הראשי שלך</p>
            <input type="password" id="masterKey" placeholder="קוד סודי (נסה 12345)">
            <button class="btn" onclick="enter()">כניסה להכל</button>
        </div>
        <script>
            function enter() {
                const key = document.getElementById('masterKey').value;
                window.location.href = '/dashboard?key=' + key;
            }
        </script>
    </body>
    </html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(key: str):
    if key not in services_data:
        return "<h1>גישה נדחתה. המפתח אינו תקין.</h1>"
    
    user = services_data[key]
    return f"""
    <html dir="rtl">
    <head>
        <style>
            body {{ font-family: sans-serif; background: #f8fafc; padding: 20px; }}
            .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 800px; margin: auto; }}
            .box {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #38bdf8; }}
            h2 {{ color: #1e293b; margin-top: 0; }}
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">שלום {user['name']}, המפתח שלך פעיל!</h1>
        <div class="grid">
            <div class="box"><h2>💰 ארנק דיגיטלי</h2><p>יתרה: {user['balance']}</p></div>
            <div class="box"><h2>📧 הודעות</h2><p>יש לך {user['notifications']} הודעות חדשות</p></div>
            <div class="box"><h2>🛠️ גישת API</h2><p>סטטוס: {user['api_access']}</p></div>
            <div class="box"><h2>⚙️ הגדרות</h2><p>המייל שלך: {user['email']}</p></div>
        </div>
    </body>
    </html>
    """
