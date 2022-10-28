# coding:utf-8
from flask import *
import requests, time, re, hashlib,string,random
import copy
import hashlib
from datetime import timedelta
def rd(n):
    t=''
    for i in range(n):t+=random.choice(string.ascii_letters)
    return t
# import geoip2.database
# reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
app = Flask(__name__)
# reader = geoip2.database.Reader('./Country.mmdb')
from flask import Flask, session
app.config["SECRET_KEY"] = rd(1024)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)

idl={}

@app.template_global()  # 定义全局模板函数
def _1(a):
    return a[0]


@app.template_global()  # 定义全局模板函数
def _2(a):
    return a[1]


@app.template_global()  # 定义全局模板函数
def _3(a):
    return a[2]


@app.template_global()  # 定义全局模板函数
def _4(a):
    return a[3]


def get_ip_addr(ip):
    global reader
    # try:
    #     response = reader.country(ip)  # 有多种语言，我们这里主要输出英文和中文print("你查询的IP的地理位置是:")
    #     if response.country.names['zh-CN'] != '中国':
    #         return response.country.names['zh-CN'], '未知', False
    #
    #     return response.country.names['zh-CN'], '未知', True
    # except:
    #     return '未知', '未知', False
    return '?'

hash_salt=rd(1024).encode()
def hash(i):
    global hash_salt
    x = hashlib.sha512(hash_salt)
    x.update(i.encode('utf-8'))
    return x.hexdigest()








    #
    # path='http://ip-api.com/json/%s'
    # try:
    #     res=requests.get(path%ip)
    #     return eval(res.text)['country'],eval(res.text)["regionName"],True
    # except:
    #     return '未知国家','未知州/省',False


# get_ip_addr('223.192.2.165')
# input()
l = {'sample': [
    ['[name]', '[message]', '[time]', '[Undefined]', '[Country]', '[Undefined]']
]}
last_create = 1

snapshot_list = {str(['null', 'hash']): [0, ['system', '...', '0000-00-00 00:00:00', 'NONE', 'China', 'None']]}
# snapshot_list=[]
snap_max = 1024
# 昵称 消息 时间 UA 国家 省

block_room = []
send_block = ['jav']
temp_lock = {'daklwjlkwa': [999999999999, 1]}
online = {'sample': 0}

private={'sample2':['system', '...', '0000-00-00 00:00:00', 'NONE', 'China', 'None']}#非公开聊天室
private_key_database={'sample2':[('fiusyeiuf',0)]}
#房间名:[(授权码:授权时间)]
private_key={'127.0.0.1':{'sample2':'fiusyeiuf'}}
private_user_key={}
notice={}

block_ip={'256.256.256.256':0}
# 房间名:上一次访问时间戳

@app.before_request
def b4():
    if session.get('id') == None:
        session['id']=rd(32)
        idl[session['id']]=request.remote_addr
        
    if session.get('hacker') == True:
        del session['hacker']
        return '温馨提示:你最近的操作可能有恶意行为，请友善使用该网站。'
    
    for i in notice.items():
        if session.get(i[0]) == None:
            session[i[0]]='1'
            return """
            <!Doctype html>
            <center>
            <h1>%s</h1>
            <h2><pre>%s</pre></h2>
            <i><small>如要访问正常功能，请刷新。</small></i>
            </center>
            """%(i[1][0],i[1][1])

    if session.get('last_time') != None:
        if time.time() - session['last_time'] > 86400:
            del idl[session['id']]
            del session['id']
            return '您超过一天未访问,服务器清空Cookies，请重新刷新此网页以重新分配一个标识符。如果您加入过非公开聊天室，您的记录也会失效，下次您重新加入的时候需要重新输入密码。'



# #     if session.get('id') not in idl:#将记录绑定在user_id
# #         
# #         idl[session['id']]=request.remote_addr

    if idl[session['id']]!=request.remote_addr:
        del idl[session['id']]
        del session['id']
        return '您的标识符发生变化，服务器已清空Cookies，请重新刷新此网页以重新分配一个标识符。如果您加入过非公开聊天室，您的记录也会失效，下次您重新加入的时候需要重新输入密码。'



    session['last_time']=time.time()

# @app.after_request
# def after(res):
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(hours=24)
#     return res

@app.route('/')
def index():


    qww = []
    for i in l.items():
        qww.append(i[0])

    online_list = []
    for i in online.items():
        if i[1] == 0:
            online_list.append([i[0], '从未'])
        else:
            online_list.append([i[0], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[1]))])
    print(online_list)
    return render_template('index.html', l=qww, online_list=online_list)


@app.route('/logon')
def logon():
    return render_template('logon.html')


@app.route('/upload', methods=["POST"])
def upload():
    global last_create
    if 'python' in request.user_agent.string:
        print('屏蔽了一个爬虫')
        time.sleep(86400)
    if time.time() - last_create < 10:
        time.sleep(1)
        print('屏蔽了一个创建请求')
        return '异常请求：创建房间过于频繁',403
        # print('屏蔽了一个创建请求')
        # time.sleep(600)
        # # last_create=time.time()
        # return '短时间内有大量创建请求，该请求已被服务器拒绝。', 403
    id = request.form.get('id')
    last_create = time.time()
    if id in l:
        return '该房间号已被注册'
    else:
        l[id] = []
        lock_the_room(id,0.5)
        return redirect('/room/' + id)


@app.route('/login', methods=["POST"])
def login():
    id = request.form.get('id')
    if id in l:
        return redirect('/room/' + id)
    else:
        return '房间不存在'


@app.route('/room/<id>')
def room(id):
    global block_room

    tips = ''
    name = request.values.get('name')
    text = request.values.get('text')
    if id in temp_lock:
        if not time.time() > temp_lock[id][0]:
            try:
                return '该房间已被锁定 %s 秒 持续到 %s 还有 %s 秒自动解除锁定' % (
                temp_lock[id][1] , time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(temp_lock[id][0])),round(temp_lock[id][0]-time.time(),3))
            except:
                return '该房间已被锁定 %s 秒 持续到 %s' % (
                    temp_lock[id][1] , '')
    if id in block_room:
        return '该房间被管理员禁止访问，请稍后重试。'
    if name == None:
        name = ''
    if text == None:
        text = ''
    if id in send_block:
        tips = '==不允许发言=='
    if id in l:
        online[id] = time.time()
        return render_template("room.html", id=id, message=l[id], name=name, text=text, tips=tips)
    else:
        return '房间不存在'


@app.route('/room/<id>/upload', methods=["POST"])
def room_upload(id):
    # global reader
    # response = reader.city(ip)
    if id in send_block:
        return "该聊天室已被管理员禁止发言"
    if id in block_room:
        return redirect('/')

    # name = request.remote_addr[:request.remote_addr.rfind('.')+1]+'*'*len(request.remote_addr[request.remote_addr.rfind('.')+1:])
    # name=hash(name)

    if session.get('id') == None:
        session['id']=rd(32)
        idl[session['id']]=request.remote_addr

    if session.get('id') != None and session.get('id') not in idl:
        session['id']=rd(32)
        idl[session['id']]=request.remote_addr

    if idl[session['id']]!=request.remote_addr:
        del idl[session['id']]
        del session['id']
        return '您的标识符发生变化，服务器已为您清空Cookies，请重新刷新此网页以重新分配一个标识符。如果您加入过非公开聊天室，您的记录也会失效，下次您重新加入的时候需要重新输入密码。'
    name=session['id']


    word = request.form.get('text')
    # ip_info = get_ip_addr(request.remote_addr)
    ip2 = request.remote_addr
    # if ip_info[2]:
    #     ip2 = '不可见'
    info = ''
    color = ''
    # if ip_info[0] != '中国':
        # info='安全提示:该消息不来自中国大陆 请仔细辨别其内容'
        # info = ''
        # color = 'black'
    ip2='UNKNOW'
    l[id].insert(0, [name, word, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '不可见', '',
                     '', ip2, info, color])
    online[id] = time.time()
    return redirect('/room/%s?name=%s' % (id, name))


@app.route('/admin')
def admin():
    return str(l)

@app.route('/clear_ip')
def clear_ip():
    for i in idl.items():
        idl[i[0]]='clear'
    return 'SUCCESS'

@app.route('/static/jquery.js')
def js():
    return render_template('jquery.js')


@app.route('/cpage/ffggf/<room_name>')
def delete(room_name):
    del l[room_name]
    return "SUCCESS"


@app.route('/cpage/ggffg/<room_name>')
def delete_message(room_name):
    l[room_name] = []
    return "SUCCESS"


@app.route('/cpage/rename/<before>/<after>')
def rename(before, after):
    l[after] = l[before]
    del l[before]
    return "OK"


@app.route('/cpage/block/<room>')
def func_block_room(room):
    block_room.append(room)
    return 'SUCCESS'


@app.route('/cpage/reblock/<room>')
def func_cancel_block_room(room):
    block_room.remove(room)
    return 'SUCCESS'


@app.route('/cpage/get/<room>')
def get_room_message_list(room):
    return l[room]


@app.route('/cpage/get_all')
def get_all_message_list():
    return l


@app.route('/cpage/lock/<room>/<s>')
def lock_the_room(room, s):
    temp_lock[room] = [time.time() + float(s), float(s)]
    return 'ok'


@app.route('/snapshot/<room>')
def snapshot(room):
    if room not in l:
        return '快照拍摄失败：房间不存在'
    if room in block_room:
        return '快照拍摄失败：无法访问聊天记录'

    if str(snapshot_list.keys()).count(room) >= snap_max:
        return '快照拍摄失败：超过设定的极限（%s张）' % snap_max
    hash_ = hash(str(l[room]))
    if str([room, hash_]) in snapshot_list:
        return '快照拍摄失败：同一快照已存在 链接为/read-snapshot/%s/%s' % (room, hash_)
    # hash_=hash(str(l[room]))
    snapshot_list[str([room, hash_])] = [time.time(), copy.deepcopy(l[room])]

    print(snapshot_list)
    return "快照拍摄成功 链接为/read-snapshot/%s/%s" % (room, hash_)


@app.route('/read-snapshot/<room>/<hash_text>')
def read_snapshot(room, hash_text):
    if str([room, hash_text]) not in snapshot_list:
        return "快照读取失败：快照不存在"
    return render_template("snapshot.html", id='', message=snapshot_list[str([room, hash_text])][1], name='', text='',
                           tips='===你正在查看房间”%s“的快照 此快照拍摄时间为%s(时间戳)===' % (
                               room, snapshot_list[str([room, hash_text])][0]))

@app.route('/del_all_room/')
def del_all_room():
    global l
    del l
    l={}
    return 'OK'


@app.route('/private-chat-room/join')
def joinp():
    return render_template('pcjoin.html')



@app.route('/private-chat-room/join/enter_id',methods=["POST"])
def enter_id():
    return redirect('/private-chat-room/chat/%s'%hash(request.form.get('id')))

@app.route('/private-chat-room/create')
def create_private_room():
    return render_template('private-chat-room-logon.html')

@app.route('/private-chat-room/create/upload',methods=["POST"])
def create_private_room_upload():
    global private
    id=hash(request.form.get('id'))
    pswd=hash(request.form.get('password'))
    print('id pswd',id)
    print(pswd)
    private[str((id,pswd))]=[]
    print('name',id)
    return redirect('/private-chat-room/chat/%s'%id)

@app.route('/private-chat-room/chat/<name>')
def join_private(name):
    return render_template('private-chat-room-join.html',id=name)

@app.route('/private-chat-room/chat/<name>/check',methods=["POST"])
def join_private_check(name):
    pswd=request.form.get('password')
    if request.form.get('password') == None:
        return '很好玩，现在，请输入密码',400
    if len(request.form.get('password'))==0:
        return '很好玩，现在，请输入密码', 400

    if str((name,hash(pswd))) not in private:
        return '密码不正确或房间不存在。',404
    p=(rd(64),time.time()+900,hash(pswd))

    if name not in private_key_database:
        private_key_database[name]=[]
    private_key_database[name].append(p)

    if session.get('private')==None:
        session['private']={}
    if type(session.get('private')) != dict:
        session['private']={}
    session['private'][name]=p

    #将记录绑定在user_id
    if session.get('id') not in private_user_key:
        private_user_key[session.get('id')]=[]
    if private_key.get(name) == None:
        private_key[name]={}
    # if session.get('id') in private_user_key:
    private_user_key[session.get('id')].append(p)
    private_key[name][p[0]]=p[1]

    return redirect('/private-chat-room/%s/chat'%name)

@app.route('/private-chat-room/<name>/chat')
def private_chat(name):
    # global session

    # print(session)

    if session.get('private')==None:
        return '无法访问此房间：您没有登录在任何房间的记录，请登录后重试。'

    if type(session.get('private')) != dict:
        session.clear()
        session['hacker']=True
        return '拒绝访问：本次请求可能含有攻击行为。'

    if session.get('private')=={}:
        return '无法访问此房间：您没有登录在任何房间的记录，请登录后重试。'

    if name not in session.get('private'):
        return '无法访问此房间：您并未在这个房间登录，请登录后重试。'

    if session.get('id') not in private_user_key:
        session.clear()
        return '拒绝访问：本次请求可能含有攻击行为。'

    # print(session.get('private'))
    # print(private_user_key[session.get('id')])
    # print(private)
    q=[]
    for i in private_user_key[session.get('id')]:
        q.append(i[0])

    if session.get('private')[name][0] not in q:
        session.clear()
        return '服务器中没有你的记录，已为您清空所有cookies'

    if private.get(str((name,session.get('private')[name][2]))) == None:
        return '您的登录已成功，但是房间可能已经失效了（无法找到房间）'

    return render_template("private-room.html", id=name, message=private.get(str((name,session.get('private')[name][2]))), name=session.get('id'), text='', tips='')



@app.route('/private-chat-room/<id>/chat/upload', methods=["POST"])
def private_room_upload(id):
    # global session
    name = session.get('id')

    if session.get('private')==None:
        return '无法访问此房间：您没有登录在任何房间的记录，请登录后重试。'

    if type(session.get('private')) != dict:
        session.clear()
        session['hacker']=True
        return '拒绝访问：本次请求可能含有攻击行为。3'

    if session.get('private')=={}:
        return '无法访问此房间：您没有登录在任何房间的记录，请登录后重试。'

    if id not in session.get('private'):
        return '无法访问此房间：您并未在这个房间登录，请登录后重试。'

    if session.get('id') not in private_user_key:
        print(session.get('id'))
        print(private_user_key)
        
        session.clear()
        return '拒绝访问：本次请求可能含有攻击行为。2'
    # print(private)

    if session.get('private').get(id)[0] not in private_key[id]:
        
        session['hacker']=True
        return '拒绝访问：本次请求可能含有攻击行为。1'
    pswd=session.get('private').get(id)[2]
    word = request.form.get('text')
    info = ''
    color = ''
    ip2='UNKNOW'
    private[str((id,pswd))].insert(0, [name, word, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '不可见', '',
                     '', ip2, info, color])
    # online[id] = time.time()
    return redirect('/private-chat-room/%s/chat' %id)







@app.route('/create_n')
def create_notice():
    return render_template('create_n.html')

@app.route('/create_n/upload',methods=["POST"])
def create_notice_upload():
    global notice
    title=request.form.get('title')
    txt=request.form.get('txt')
    notice[rd(32)]=(title,txt)
    return 'SUCCESS'

@app.route('/get_n')
def get_n():
    return str(notice)

@app.route('/del_n/<name>')
def del_n(name):
    global notice
    del notice[name]
    return 'SUCCESS'

@app.route('/update_log')
def update_log():
    return """
    <pre>
    <h1>更新日志</h1>
    2022-10-25 N.1-Full（项目实际在2022-10-27全部完成）
    新增功能:
        创建非公开聊天室
    </pre>
    """
#
# @app.route('/set/<name>/<value>')
# def set_var(name,value):
#     session[name]=eval(value)
#     print('set',name,type(value),value)
#     return 'OK'


@app.route('/conduct')
def conduct():
    return """
    聊天行为规范
    
    这是一个匿名聊天网站，但是我还是希望你能遵守以下内容。
    不要讨论儿童色情内容。
    不要贩卖东西。
    不要搞诈骗。
    
    被我发现聊一些不好的东西我会立刻封停房间（30分钟到24小时不等）
    其他的我不管。
    
    
    
    """.replace('\n','<br/>')


if __name__ == '__main__':
    app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    app.run(host='0.0.0.0',port=80,debug=True)
