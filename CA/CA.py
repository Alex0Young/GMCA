import time

from flask import Flask, render_template
from flask import request, url_for, session, redirect
import os
from flask import flash
from configparser import ConfigParser
from functools import wraps
from config import *

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)


# 装饰器，用于判断用户是否在登录状态
def login_requried(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('login_in'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper

#检查sub-ca请求信息是否正确
def checkInfo(pwd, info):
    print(pwd)
    print(info)
    if pwd[0] == pwd[1]:
        for i in range(0, 6):
            if info[i] == '':
                return 0
    else:
        return 0
    return 1


# 编辑 sub-ca.conf
def configSubCA(info):
    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    config_file = '{dir}/sub-ca.conf'.format(dir=basedir)
    cp = ConfigParser()
    cp.read(config_file)
    cp.set('ca_dn', 'countryName', info[0])
    cp.set('ca_dn', 'stateOrProvinceName', info[1])
    cp.set('ca_dn', 'localityName', info[2])
    cp.set('ca_dn', 'organizationName', info[3])
    cp.set('ca_dn', 'organizationalUnitName', info[4])
    cp.set('ca_dn', 'commonName', info[5])
    cp.set('ca_dn', 'emailAddress', info[6])
    with open(config_file, 'w+') as config_file:
        cp.write(config_file)

#获取sub-ca.conf
def getConfig():
    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    config_file = 'sub-ca.conf'
    cp = ConfigParser()
    cp.read(config_file)
    info = []
    info.append(cp.get('ca_dn', 'countryName'))
    info.append(cp.get('ca_dn', 'stateOrProvinceName'))
    info.append(cp.get('ca_dn', 'localityName'))
    info.append(cp.get('ca_dn', 'organizationName'))
    info.append(cp.get('ca_dn', 'organizationalUnitName'))
    info.append(cp.get('ca_dn', 'commonName'))
    info.append(cp.get('ca_dn', 'emailAddress'))
    return info


# 初始化 sub_ca 环境，创建文件夹，复制配置文件
def initEV():
    # prepare dirs
    cmd1 = 'mkdir sub_ca_{name}'
    cmd2 = 'mkdir sub_ca_{name}/certs'
    cmd3 = 'mkdir sub_ca_{name}/newcerts'
    cmd4 = 'mkdir sub_ca_{name}/crl'
    cmd5 = 'mkdir sub_ca_{name}/private'
    cmd6 = 'mkdir sub_ca_{name}/db'
    cmd12 = 'mkdir sub_ca_{name}/csr'
    # prepare config
    cmd7 = 'echo 01 > sub_ca_{name}/serial'
    cmd8 = 'touch sub_ca_{name}/index.txt'
    cmd9 = 'touch sub_ca_{name}/db/index.attr'
    cmd10 = 'chmod 700 sub_ca_{name}/private'
    cmd11 = 'cp sub-ca.conf sub_ca_{name}/'
    os.system(cmd1.format(name=session['user_id']))
    os.system(cmd2.format(name=session['user_id']))
    os.system(cmd3.format(name=session['user_id']))
    os.system(cmd4.format(name=session['user_id']))
    os.system(cmd5.format(name=session['user_id']))
    os.system(cmd6.format(name=session['user_id']))
    os.system(cmd7.format(name=session['user_id']))
    os.system(cmd8.format(name=session['user_id']))
    os.system(cmd9.format(name=session['user_id']))
    os.system(cmd10.format(name=session['user_id']))
    os.system(cmd11.format(name=session['user_id']))
    os.system(cmd12.format(name=session['user_id']))


# 生成 sub-ca 请求
def gen_subCA(enpwd, info):
    # gen sm2 key
    basedir = 'sub_ca_{name}/'.format(name=session['user_id'])
    # cmd1 = 'openssl ecparam -genkey -name SM2 -out private/sub-ca.key'
    # cmd2 = 'openssl req -new -config {dir}/sub-ca.conf -key private/sub-ca.key -out sub-ca.csr'
    cmd1 = 'gmssl ecparam -genkey -name sm2p256v1 -out private/sub-cakey.pem'
    cmd2 = 'gmssl req -new -sm3 -key private/sub-cakey.pem -out sub-cacsr.pem'
    os.system(cmd1)
    os.system(cmd2)
    return 1

#初始化sub-ca
def init_CA(enpwd, info):
    initEV()
    basedir = 'sub_ca_{name}'.format(name=session['user-id'])
    cwd = os.getcwd()
    if cwd.find(basedir) < 0:
        os.chdir(basedir)

    check1 = "csr"
    if os.path.exists(check1):
        configSubCA(info)
        res = gen_subCA(enpwd, info)
        check2 = "sub-cacsr.pem"
        if os.path.exists(check2):
            return 1
        else:
            return 0
    else:
        return 0

#获取所有待ca签名的请求
def getCsr():
    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    cwd = os.getcwd()
    print('cwd:', cwd)
    if cwd.find(basedir) < 0:
        os.chdir(basedir)
        print('ss')
    print(os.getcwd())
    csrDir = 'csr'
    csrlist = os.listdir(csrDir)
    csrinfo = []
    cmd1 = 'openssl req -subject -noout -in {dir}/{csr} > data'
    for i in range(0, len(csrlist)):
        con = []
        if csrlist[i] != 'data':
            csr = csrlist[i].split('+')
            con.append(csr[1])
            con.append(csr[0])
            os.system(cmd1.format(dir=csrDir, csr=csrlist[i]))
            fp = open('data', 'r')
            data = fp.readlines()
            con.append(data)
            csrinfo.append(con)
    return csrinfo


#对用户证书请求签名
def signReq(reqName,vadays):
    reqN = reqName.split('.')
    reque = reqN[0].split('+')
    print("reqN:", reqN)
    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    # change working dir
    # os.chdir(basedir)
    # sign client req
    # cmd1 = 'openssl ca -batch -config sub-ca.conf -in csr/{req}.csr -out newcerts/{req}.crt -extensions server_ext'.format(
    #     req=reqN[0])
    reqcert = reqN[0][:-3]
    cmd1 = 'gmssl ca -batch -md sm3 -extensions v3_ca -in csr/{reqcsr}.pem -out newcerts/{reqcert}cert.pem -days {day} -cert sub-cacert.pem -keyfile private/sub-cakey.pem'.format(reqcsr=reqN[0],reqcrt=reqcert,day=vadays)
    os.system(cmd1)
    # combine sub-ca.crt
    cmd2 = 'cat sub-ca.crt >> newcerts/{reqcrt}cert.pem'.format(reqcrt=reqcert)
    os.system(cmd2)
    crtname = 'newcerts/{reqcrt}.pem'.format(reqcrt=reqcert)
    if os.path.isfile(crtname):
        cmd3 = 'rm csr/{reqcsr}.pem'.format(req=reqN[0])
        os.system(cmd3)
        print('sign success')
        return 1
    else:
        return 0

#获取所有已发布生成的证书
def getCrt():
    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    cwd = os.getcwd()
    if cwd.find(basedir) < 0:
        os.chdir(basedir)
    crtDir = 'newcerts'
    crtlist = os.listdir(crtDir)
    print('crtlist:', crtlist)
    crtinfo = []
    cmd1 = 'openssl x509 -subject -in {dir}/{crt} > data'
    for i in range(0, len(crtlist)):
        con = []
        if crtlist[i] != 'data' and crtlist[i].find('cert') > 0:
            crt = crtlist[i].split('+')
            con.append(crt[1])
            con.append(crt[0])
            os.system(cmd1.format(dir=crtDir, crt=crtlist[i]))
            fp = open('data', 'r')
            data = fp.readline()
            con.append(data)
            crtinfo.append(con)
            print('crtinfo:', crtinfo)
    return crtinfo


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('login_in') != True:
        return redirect(url_for('login'))

    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    cwd = os.getcwd()
    print('index:', cwd)
    if cwd.find(basedir) > 0:
        # os.chdir(basedir)
        certfile = 'sub-cacert.pem'
        csrfile = 'sub-cacsr.pem'
    else:
        certfile = '{dir}/sub-cacert.pem'.format(dir=basedir)
        csrfile = '{dir}/sub-cacsr.pem'.format(dir=basedir)
    # print('log 1',certfile)
    if os.path.isfile(certfile):
        if cwd.find(basedir) < 0:
            os.chdir(basedir)
        info = []
        info = getConfig()
        print("getinfo:", info[3], info[4], info[5], info[6])
        flag = 1
        return render_template('index.html', **locals())
    elif os.path.isfile(csrfile):
        if cwd.find(basedir) < 0:
            os.chdir(basedir)
        info = []
        info = getConfig()
        print("info:", info)
        flag = 0
        return render_template('index.html', **locals())
    else:
        print('log 2')
        return render_template('initca.html')
    #         return render_template('index.html')
    # return render_template('index.html')


@app.route('/initCA', methods=['GET', 'POST'])
def initCA():
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
            flag = 0
            return render_template('initca.html', **locals())
        else:
            flash('输入正确')
            print('ok')
            # init sub_CA
            res = init_CA(enpwd, info)
            if res == 1:
                print('ca init success')
                flag = 2
                return redirect(url_for('index'))
            else:
                print('ca init failed')
                flag = 0
                return render_template('initca.html', **locals())
    return render_template('initca.html')

#发布证书，发布的证书信息需要存储进入数据库
@app.route('/issue', methods=['GET', 'POST'])
def issue():
    csrinfo = []
    csrinfo = getCsr()
    if request.method == 'POST':
        vaddays = request.form['validation_days']
        time = request.form['time']
        name = request.form['name']
        csrname = name + '+' + time
        print('csrname:', csrname)
        print("vaddays:", vaddays)
        res = signReq(csrname,vaddays)
        return redirect(url_for('issue'))

    return render_template('issue.html', **locals())


@app.route('/validate')
def validate():
    return render_template('validate.html')


@app.route('/list')
def list():
    crtinfo = []
    crtinfo = getCrt()
    return render_template('list.html', **locals())


# get the current user cert file path
# if the file exist, return file cert file path and csr file path
# else return both None
def get_cert_file_path():
    if session.get('login_in') != True:
        return redirect(url_for('login'))

    basedir = 'sub_ca_{name}'.format(name=session['user_id'])
    cwd = os.getcwd()
    print('index:', cwd)
    if cwd.find(basedir) > 0:
        certfile = 'sub-ca.crt'
        csrfile = 'sub-ca.csr'
    else:
        certfile = '{dir}/sub-ca.crt'.format(dir=basedir)
        csrfile = '{dir}/sub-ca.csr'.format(dir=basedir)

    if os.path.isfile(certfile):
        return certfile, csrfile
    else:
        return None, None

# get the serial ,subjectinformation from cert file
# if path exist return serial and subject
# else return both None
# path is the cert path
def get_destroy_crt_info(path):
    if os.path.isfile(path):
        cmd = 'openssl x509 -in {path} -noout -serial -subject'.format(path=path)
        res = os.popen(cmd).readlines()
        serial = res[0].strip().split("=")[-1]
        subject = res[1].strip()[8:].replace(" ", "").split(",")
        return serial, subject
    else:
        return None, None


# get the cert status
# if serial exist in index database, return cert status
# else return None
def cert_is_revoke(serial, subject):
    with open(root_database, "r") as f:
        res = f.readlines()
    for line in res:
        line = line.strip().split("\t")
        tmp_status = line[0]
        tmp_serial = line[3]
        tmp_subject = line[5][1:].split("/")
        if tmp_serial == serial and tmp_subject == subject:
            if tmp_status == "V":
                return False
            elif tmp_status == "R":
                return True
    return False

# need user cert file path
@app.route('/destroy')
def destroy():
    cert_file, csr_file = get_cert_file_path()
    if cert_file is not  None and csr_file is not None:
        path = "tmp"
        serial, subject = get_destroy_crt_info(cert_file)
        user_serial, user_subject = get_destroy_crt_info(path)
        if serial==user_serial and subject ==  user_subject:
            pem_path = root_cert + serial.split("=")[-1] + ".pem"
            if cert_is_revoke(serial, subject):
                msg = "the cert has already been revoked"
            else:
                msg = "revoke success"
                cmd = "openssl ca -revoke {path}".format(path=pem_path)
                os.system(cmd)
                time.sleep(1)
                if cert_is_revoke(serial, subject):
                    msg = "revoke failed, please try again later"
                else:
                    # update revoke list
                    pass
        else:
            msg = "cert file information is not correct, please try again"

    else:
        msg = "cert not found, please create cert first!"
    return render_template('destroy.html', **locals())


#登录，无注册，登录用户密码需要从数据库获取
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
        elif name == 'admin' and pwd == 'admin':
            session['user_id'] = name
            session['pwd'] = pwd
            session['login_in'] = True
            print('111')
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

