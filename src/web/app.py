from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

app = Flask(__name__)
app.secret_key = 'lucky_draw_secret_key'  # 用于 flash 消息

# CSV 文件路径
PARTICIPANTS_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/participants.csv'))

@app.route('/', methods=['GET'])
def index():
    """显示主页，包含用户填写表单"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """处理表单提交"""
    department = request.form.get('department', '').strip()
    name = request.form.get('name', '').strip()
    
    # 简单的表单验证
    if not department or not name:
        flash('部门和姓名都是必填项！', 'error')
        return redirect(url_for('index'))
    
    # 写入 CSV 文件
    try:
        # 检查文件是否存在，如果不存在则创建并写入标题行
        file_exists = os.path.isfile(PARTICIPANTS_CSV)
        
        with open(PARTICIPANTS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # 如果文件不存在，写入标题行
            if not file_exists:
                writer.writerow(['department', 'name'])
            
            # 写入新的参与者数据
            writer.writerow([department, name])
        
        flash(f'成功添加参与者: {name} ({department})', 'success')
    except Exception as e:
        flash(f'添加参与者时出错: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/participants', methods=['GET'])
def view_participants():
    """显示所有参与者列表"""
    participants = []
    
    try:
        if os.path.isfile(PARTICIPANTS_CSV):
            with open(PARTICIPANTS_CSV, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                participants = list(reader)
    except Exception as e:
        flash(f'读取参与者列表时出错: {str(e)}', 'error')
    
    return render_template('participants.html', participants=participants)

if __name__ == '__main__':
    # 确保 data 目录存在
    os.makedirs(os.path.dirname(PARTICIPANTS_CSV), exist_ok=True)
    app.run(debug=True)