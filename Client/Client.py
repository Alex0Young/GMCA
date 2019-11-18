from flask import Flask,render_template
from flask import request, url_for, session,redirect
import os
from flask import flash

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)

#装饰器，用于判断用户是否在登录状态
def login_requried(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('login_in'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

def checkInfo(pwd,info):
    print(pwd)
    print(info)
    if pwd[0] == pwd[1]:
        for i in range(0,6):
            if info[i] == '':
                return 0
    else:
        return 0
    return 1

def gen_key(enpwd, info):
    os.system("openssl ecparam -genkey -name SM2 -out ")


@app.route('/', methods=['GET', 'POST'])
def index():
    print ('hhh')
    if session.get('login_in') != True:
        return redirect(url_for('login'))
    if request.method == 'POST':
        enpwd = []
        enpwd.append(request.form['password'])
        enpwd.append(request.form['confirm_password'])
        info = []
        info.append(request.form['country_name'])
        info.append(request.form['state_name'])
        info.append(request.form['loc_name'])
        info.append(request.form['org_name'])
        info.append(request.form['unit_name'])
        info.append(request.form['common_name'])
        info.append(request.form['email'])
        check = checkInfo(enpwd, info)
        if check == 0:
            flash('输入错误，请检查密码和输入信息')
            print('false')
        else:
            flash('输入正确')
            print('ok')

        return render_template('index.html')
    return render_template('index.html')
@app.route('/issue')
def issue():
    return render_template('issue.html')
@app.route('/validate')
def validate():
    return render_template('validate.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/destroy')
def destroy():
    return render_template('destroy.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        pwd = request.form['password']

        if name == '' or pwd == '':
            return render_template('login.html')
        elif name == 'username' and pwd == 'admin':
            session['user_id'] = name
            session['pwd'] = pwd
            session['login_in'] = True
            print('111')
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


if __name__ == '__main__':
    app.run()

