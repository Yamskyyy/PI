import os
from os.path import join, dirname
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
import hashlib
import uuid
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'SPARTA'
TOKEN_KEY = 'mytoken'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client=MongoClient('mongodb+srv://Aryama:1234@cluster0.9x3eatx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db=client.dbOrderKerja

app = Flask(__name__)

@app.route("/")
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    if token_receive:
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = db.normal_users.find_one({'username': payload.get('id')})
            user_info2 = db.expert_users.find_one({'username': payload.get('id')})
            user_info3 = db.dept_users.find_one({'username': payload.get('id')})
            order=list(db.order.find({}))

            if user_info:
                return render_template('dashboard.html',user_info=user_info, order=order)
            elif user_info2:
                return render_template('order.html',user_info2=user_info2, order=order)
            elif user_info3:
                return render_template('departemen.html',user_info3=user_info3, order=order)
            else:
                return render_template('login.html')

        except jwt.ExpiredSignatureError:
            msg = 'Your token has expired'
            return redirect(url_for('login', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'There was a problem logging you in'
            return redirect(url_for('login', msg=msg))
    else:
        return render_template('login.html')

    
@app.route('/dashboard',methods=['GET'])
def dashboard():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    order=list(db.order.find({}))
    return render_template('dashboard.html', order=order)

@app.route('/dashboard_user',methods=['GET'])
def dashboard_user():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    order=list(db.order.find({}))
    return render_template('dashboard_user.html', order=order)

@app.route("/login")
def login():
    token_receive = request.cookies.get(TOKEN_KEY)
    msg = request.args.get("msg")
    if msg:
        return render_template('login.html',msg=msg)
    else:
        if token_receive:
            try:
                payload = jwt.decode(
                    token_receive,
                    SECRET_KEY,
                    algorithms=['HS256']
                )
                user_info = db.normal_users.find_one({'username': payload.get('id')})
                user_info2 = db.expert_users.find_one({'username': payload.get('id')})
                user_info3 = db.dept_users.find_one({'username': payload.get('id')})
                order=list(db.order.find({}))

                if user_info:
                    return render_template('dashboard.html',user_info=user_info, order=order)
                elif user_info2:
                    return render_template('order.html',user_info2=user_info2, order=order)
                elif user_info3:
                    return render_template('departemen.html',user_info3=user_info3, order=order)
                else:
                    return render_template('login.html')
                    
            except jwt.ExpiredSignatureError:
                msg='Your token has expired'
                return redirect(url_for('login', msg=msg))
            except jwt.exceptions.DecodeError:
                msg='There was a problem logging you in'
                return redirect(url_for('login', msg=msg))
        else:
            return render_template('login.html',msg=msg)



@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    print(username_receive, pw_hash)
    result = db.normal_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    result2 = db.expert_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    result3 = db.dept_users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    elif result2:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    elif result3:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )


@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    role_receive = request.form["role_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    if(role_receive == 'expert'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,                                  
            "profile_name": username_receive,
            "role":role_receive,                                            
            }
        db.expert_users.insert_one(doc)
        return jsonify({'result': 'success'})
    elif(role_receive == 'dept'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,                                  
            "profile_name": username_receive,
            "role":role_receive,                                            
            }
        db.dept_users.insert_one(doc)
        return jsonify({'result': 'success'})
    elif(role_receive == 'normal'):
        doc = {
            "username": username_receive,                               
            "password": password_hash,
            "profile_name" : username_receive,     
            "role":role_receive,                                                                        
            }
        db.normal_users.insert_one(doc)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failed'})


@app.route("/sign_up/check_dup", methods=["POST"])
def check_dup():
    # ID we should check whether or not the id is already taken
    username_receive = request.form["username_give"]
    exists = bool(db.normal_users.find_one({'username':username_receive}))
    exists2 = bool(db.expert_users.find_one({'username':username_receive}))
    exists3 = bool(db.dept_users.find_one({'username':username_receive}))
    return jsonify({"result": "success", "exists": exists+exists2+exists3})

@app.route('/order',methods=['GET'])
def order():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    order=list(db.order.find({}))
    return render_template('order.html', order=order)

@app.route('/order_admin', methods=['GET', 'POST'])
def order_admin():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    order=list(db.order.find({}))
    return render_template('order_admin.html', order=order)

@app.route('/AddOrder',methods=['GET', 'POST'])
def AddOrder():
    if request.method=='POST':
        nama = request.form['nama']
        dari = request.form['dari']
        untuk = request.form['untuk']
        deskripsi = request.form['deskripsi']
        count = db.order.count_documents({})
        num = count + 1

        # Menyimpan gambar
        gambar = request.files['gambar']
        extension = gambar.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%M-%d:%H-%m-%S')
        gambar_name = f'gambar-{mytime}.{extension}'
        save_to = f'static/assets/Imgorder/{gambar_name}'
        gambar.save(save_to)

        # Menambahkan tanggal
        tanggal = today.strftime('%d-%m-%Y')
        
        # Membuat ID
        order_date = today.strftime('%d%m%Y')
        order_id = f'OK/{num}/{order_date}'

        # Membuat dokumen
        doc = {
            'id': order_id,
            'num': num,
            'nama': nama,
            'dari': dari,
            'untuk': untuk,
            'deskripsi': deskripsi,
            'gambar': gambar_name,
            'status': 'Menunggu Persetujuan',
            'Alasan': '-',
            'tanggal': tanggal,  # Menambahkan field tanggal
            'konfirmasi': '-'
        }

        db.order.insert_one(doc)
        return redirect(url_for('order'))
    return render_template('AddOrder.html')

@app.route('/EditOrder/<_id>',methods=['GET', 'POST'])
def EditOrder(_id):
    if request.method=='POST':
        nama = request.form['nama']
        dari = request.form['dari']
        untuk = request.form['untuk']
        deskripsi = request.form['deskripsi']

        gambar=request.files['gambar']
        extension= gambar.filename.split('.')[-1]
        today=datetime.now()
        mytime=today.strftime('%Y-%M-%d:%H-%M-%S')
        gambar_name = f'gambar-{mytime}.{extension}'
        save_to = f'static/assets/Imgorder/{gambar_name}'
        gambar.save(save_to)
        
        # Menambahkan tanggal
        tanggal = today.strftime('%d-%m-%Y')

        doc = {
            'nama' : nama,
            'dari' : dari,
            'untuk' : untuk,
            'deskripsi' : deskripsi,
            'tanggal': tanggal 
        }
        if gambar:
            doc['gambar']=gambar_name
        db.order.update_one({'_id': ObjectId(_id)}, {'$set':doc})
        return redirect(url_for('order'))
    id = ObjectId(_id)
    data = list(db.order.find({'_id': id}))

    return render_template('EditOrder.html', data=data)  

@app.route('/deleteorder/<_id>', methods=['GET', 'POST'])
def delete(_id): 
    id = ObjectId(_id)
    db.order.delete_one({'_id':id})
    return redirect(url_for('order'))

@app.route("/approve", methods=["POST"])
def approve():
    num_receive = request.form['num_give']
    today = datetime.now()
    tanggal = today.strftime('%Y-%m-%d')
    db.order.update_one(
        {'num': int(num_receive)},
        {'$set': {'status': f'DISETUJUI pada {tanggal}'}}
    )
    return jsonify({'msg': 'update done!'})

@app.route("/reject", methods=["POST"])
def reject():
    num_receive = request.form['num_give']
    alasan_receive = request.form['alasan']
    today = datetime.now()
    tanggal = today.strftime('%d-%m-%Y')
    db.order.update_one(
        {'num': int(num_receive)},
        {'$set': {'status': f'DITOLAK pada {tanggal}', 'Alasan' : alasan_receive}}
    )
    return jsonify({'msg': 'update done!'})

@app.route("/selesai", methods=["POST"])
def selesai():
    num_receive = request.form['num_give']
    today = datetime.now()
    tanggal = today.strftime('%d-%m-%Y')
    db.order.update_one(
        {'num': int(num_receive)},
        {'$set': {'konfirmasi': f'Order Kerja telah DISELESAIKAN pada {tanggal}'}}
    )
    return jsonify({'msg': 'update done!'})



if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)