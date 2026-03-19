import os, io, json, base64, requests
from datetime import timedelta
from flask import Flask, request, jsonify, send_from_directory, session
from PIL import Image
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from difflib import get_close_matches

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
app.secret_key = 'flora_vi_final_2026'
app.config.update(SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=False, PERMANENT_SESSION_LIFETIME=timedelta(days=7))

# --- API GOOGLE ---
GEMINI_API_KEY = "AIzaSyCqJUJUv8TId5hQlREHUh0jTvAeHVInYQw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def call_ai(payload):
    res = requests.post(GEMINI_URL, json=payload, timeout=30)
    return res.json()['candidates'][0]['content']['parts'][0]['text']

# --- DATABASE ---
DB_CONFIG = {'host': 'nhandienhoa-tnut-8a16.f.aivencloud.com', 'port': 12281, 'user': 'avnadmin', 'password': 'AVNS_bQ5NL35Yjo4Xv8DmznL', 'database': 'FlowerDB', 'ssl_ca': 'ca.pem'}
def get_db(): return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def serve_index(): return send_from_directory('.', 'index.html')

# --- AUTH ---
@app.route('/api/register', methods=['POST'])
def register():
    d = request.json; hpw = bcrypt.generate_password_hash(d['matkhau']).decode('utf-8')
    try:
        conn = get_db(); cur = conn.cursor()
        cur.execute("INSERT INTO NguoiDung (tendangnhap, matkhau, hoten) VALUES (%s, %s, %s)", (d['tendangnhap'], hpw, d['hoten']))
        conn.commit(); conn.close(); return jsonify({'status': 'ok'})
    except: return jsonify({'error': 'Trùng tên đăng nhập'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    d = request.json; conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM NguoiDung WHERE tendangnhap = %s", (d['tendangnhap'],))
    u = cur.fetchone()
    if u and bcrypt.check_password_hash(u['matkhau'], d['matkhau']):
        session.permanent = True; session['user_id'] = u['id']; session['fullname'] = u['hoten']
        return jsonify({'user': u})
    return jsonify({'error': 'Sai tài khoản'}), 401

@app.route('/api/profile', methods=['GET'])
def profile():
    uid = session.get('user_id')
    if not uid: return jsonify({'error': 'No'}), 401
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, tendangnhap, hoten, ngaytao FROM NguoiDung WHERE id = %s", (uid,))
    return jsonify(cur.fetchone())

@app.route('/api/logout', methods=['POST'])
def logout(): session.clear(); return jsonify({'msg': 'Out'})

# --- FLOWER FEATURES (VIETNAMESE FILTERS) ---
@app.route('/api/flowers', methods=['GET'])
def get_flowers():
    uid = session.get('user_id', 0)
    q = request.args.get('q', '').strip().lower()
    color = request.args.get('color', ''); ho = request.args.get('ho', '')

    conn = get_db(); cur = conn.cursor(dictionary=True)
    sql = "SELECT h.*, (SELECT COUNT(*) FROM YeuThich WHERE id_nguoidung = %s AND id_hoa = h.id) as is_fav FROM Hoa h WHERE 1=1"
    params = [uid]
    
    if color: sql += " AND mausac = %s"; params.append(color)
    if ho: sql += " AND ho = %s"; params.append(ho)

    cur.execute(sql, tuple(params)); rows = cur.fetchall()

    if q:
        names = [r['tenhoa'].lower() for r in rows]
        matches = get_close_matches(q, names, n=20, cutoff=0.2) # Tăng độ rộng để tìm sai chính tả tốt hơn
        rows = [r for r in rows if r['tenhoa'].lower() in matches]
    
    conn.close(); return jsonify(rows)

@app.route('/api/metadata', methods=['GET'])
def get_meta():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT DISTINCT mausac FROM Hoa WHERE mausac IS NOT NULL"); colors = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT DISTINCT ho FROM Hoa WHERE ho IS NOT NULL"); hos = [r[0] for r in cur.fetchall()]
    conn.close(); return jsonify({'colors': colors, 'hos': hos})

# --- OTHERS ---
@app.route('/api/favorites/toggle', methods=['POST'])
def toggle_fav():
    uid = session.get('user_id'); hid = request.json.get('id_hoa')
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM YeuThich WHERE id_nguoidung = %s AND id_hoa = %s", (uid, hid))
    if cur.fetchone():
        cur.execute("DELETE FROM YeuThich WHERE id_nguoidung = %s AND id_hoa = %s", (uid, hid)); st = "removed"
    else:
        cur.execute("INSERT INTO YeuThich (id_nguoidung, id_hoa) VALUES (%s, %s)", (uid, hid)); st = "added"
    conn.commit(); conn.close(); return jsonify({'status': st})

@app.route('/api/favorites', methods=['GET'])
def get_favs():
    uid = session.get('user_id')
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT h.* FROM Hoa h JOIN YeuThich y ON h.id = y.id_hoa WHERE y.id_nguoidung = %s", (uid,))
    rows = cur.fetchall(); conn.close(); return jsonify(rows)

@app.route('/api/recognize', methods=['POST'])
def recognize():
    uid = session.get('user_id'); b64 = request.json.get('image_base64')
    encoded = b64.split(",")[1] if "," in b64 else b64
    payload = {"contents": [{"parts": [{"text": "Nhận diện hoa. Trả về JSON: {\"name\":\"...\",\"family\":\"...\",\"description\":\"...\",\"care\":\"...\"}."}, {"inline_data": {"mime_type": "image/jpeg", "data": encoded}}]}]}
    res = call_ai(payload); clean = res.replace("```json","").replace("```","").strip()
    if uid:
        conn = get_db(); cur = conn.cursor()
        cur.execute("INSERT INTO LichSuNhanDien (id_nguoidung, hinh_base64, ketqua_json) VALUES (%s, %s, %s)", (uid, b64, clean))
        conn.commit(); conn.close()
    return jsonify(json.loads(clean))

@app.route('/api/chat', methods=['POST'])
def chat():
    d = request.json
    p = f"Bạn là chuyên gia tư vấn Flora AI. Câu hỏi: {d['message']}"
    return jsonify({'reply': call_ai({"contents": [{"parts": [{"text": p}]}]})})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)
