from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-platform-secret-key'

CORS(app, supports_credentials=True)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'vortex'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': '需要登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    print(f"登录请求: username={username}, password={password}")
    
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and user['password'] == hash_password(password):
            # 设置session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            print(f"登录成功，用户: {user['username']}")
            return jsonify({
                'message': '登录成功',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                }
            })
        else:
            return jsonify({'message': '用户名或密码错误'}), 401
    except Exception as e:
        return jsonify({'message': f'登录失败: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# 获取用户信息
@app.route('/api/user/info', methods=['GET'])
@login_required
def get_user_info():
    return jsonify({
        'user': {
            'id': session['user_id'],
            'username': session['username'],
            'role': session['role']
        }
    })

# 退出登录
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': '退出登录成功'})

# 添加测试用例
@app.route('/api/testcase', methods=['POST'])
@login_required
def add_testcase():
    print("收到POST请求添加测试用例")
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description', '')
    steps = data.get('steps', '')
    expected_result = data.get('expected_result', '')
    
    if not title:
        return jsonify({'message': '用例标题不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO test_cases (title, description, steps, expected_result, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, steps, expected_result, session['user_id']))
        
        conn.commit()
        return jsonify({'message': '测试用例添加成功'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'添加失败: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

# 获取测试用例列表
@app.route('/api/testcase', methods=['GET'])
@login_required
def get_testcases():
    print("收到GET请求获取测试用例列表")
    print(f"当前session用户: {session.get('username')}")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT tc.*, u.username as creator_name
            FROM test_cases tc
            LEFT JOIN users u ON tc.created_by = u.id
            ORDER BY tc.created_at DESC
        """)
        testcases = cursor.fetchall()
        
        print(f"查询到 {len(testcases)} 条测试用例")
        return jsonify({'testcases': testcases})
    except Exception as e:
        print(f"数据库查询错误: {e}")
        return jsonify({'message': f'获取用例失败: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)