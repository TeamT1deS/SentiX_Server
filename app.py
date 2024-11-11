from flask import Flask, session, request, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://192.168.123.59:5173"], supports_credentials=True)
app.secret_key = '8b3d00b0ba793a5a711361773171c971db8aa2bf8a8a057b'

# 使用 SQLAlchemy 配置 MySQL 数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:T1deS%40a11a10ng@localhost:30000/sentinelx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 配置 Flask-Session 以使用 SQLAlchemy 进行会话存储
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # 或 'None' (若在跨站环境下使用)
app.config['SESSION_COOKIE_SECURE'] = False  # 在开发中关闭，生产环境可以设为 True（HTTPS 环境）

# 初始化 Flask-Session
Session(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # 验证用户名和密码（示例中直接通过）
    if username == 'admin' and password == 'admin':
        isAdmin = True
        session['user_id'] = 1
        session['username'] = username
        session['is_admin'] = isAdmin
        return jsonify(message='Logged in successfully', isAdmin=isAdmin, userName=username), 200
    if username == 'sentix' and password == 'sentix':
        isAdmin = False
        session['user_id'] = 1
        session['username'] = username
        session['is_admin'] = isAdmin
        return jsonify(message='Logged in successfully', isAdmin=isAdmin, userName=username), 200
    return jsonify(message='Invalid credentials'), 401

@app.route('/current-user', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify(isLoggedIn=True, isAdmin=session['is_admin'], userName=session['username'])
    return jsonify(isLoggedIn=False)

@app.route('/logout', methods=['POST'])
def logout():
    # print(session)
    # session.pop('user_id', None)
    session.clear()
    return jsonify(message='Logged out successfully'), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)