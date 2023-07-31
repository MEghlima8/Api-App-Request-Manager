from App import config
from flask import Flask, request, render_template, session, make_response, abort
from App.Controller.email_controller import Email
from App.Controller.user_controller import User
from App.Controller import get_request
from App.Controller import send_request
from App.Controller import process
from App.Controller import admin
from App.Controller.jwt import Token
from App.Controller import db_postgres_controller as db
from App.Controller.api_controller import api
from datetime import datetime
import json
import threading
import uuid
from pydub import AudioSegment
from io import BytesIO
import requests
from PIL import Image
import time

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = int(config.configs['SEND_FILE_MAX_AGE_DEFAULT'])
app.secret_key = config.configs['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def check_token():
    # Get Token  
    access_token = request.cookies.get('access_token')    
    # Get id
    result = Token(token=access_token).handle_token()
        
    try:    
        # Check Token is valid
        user_id = int(result)      
        res = {"result":{"user_id":user_id} , "status-code":200}
    except:
        # Token is invalid.
        res = {"result":result , "status-code":401}
    return res    


def check_token_and_add_req_to_db():
    # Get Token
    try:
        access_token = request.headers.get('Authorization').split()[1]
    except:
        access_token = request.headers.get('Authorization')
        if access_token is None:
            access_token = request.cookies.get('access_token')
    # Get id
    result = Token(token=access_token).handle_token() 
    try:    
        # Check Token is valid
        user_id = int(result)
        s_req_id = add_to_db(user_id)
        res = {"result":{"request_id":s_req_id, "user_id":user_id} , "status-code":200}        
    except:
        # Token is invalid.
        res = {"result":result , "status-code":401}        
    return res    


# Admin
@app.route('/admin-res-add-calc', methods = ['POST'])
def admin_res_add_calc():
    return admin.res_add_calc()

@app.route('/admin-res-steg-img', methods = ['POST'])
def admin_res_steg_img():
    return admin.res_steg_img()

@app.route('/admin-res-extr-steg-img', methods = ['POST'])
def admin_res_extr_steg_img():
    return admin.res_extr_steg_img()

@app.route('/admin-res-steg-audio', methods = ['POST'])
def admin_res_steg_audio():
    return admin.res_steg_audio()

@app.route('/admin-res-extr-audio', methods = ['POST'])
def admin_res_extr_audio():
    return admin.res_extr_audio()

@app.route('/admin-users-info', methods = ['POST'])
def admin_users_info():
    return admin.users_info()
# Admin

# Saves the image taken from the API request
def save_image_from_api(image_url):
    # Get image from URL
    response = requests.get(image_url)
    img_steg_new_req_img = Image.open(BytesIO(response.content))
    response.raise_for_status()

    img_name = uuid.uuid4().hex + '.png'  # Generate random name for image
    output_path = '.' + config.configs["UPLOAD_IMAGE_AFTER_HIDE"] + img_name
    img_steg_new_req_img.save(output_path)
    
    req_protocol = config.configs['REQUEST_PROTOCOL']
    dom_address = config.configs['DOMAIN_ADDRESS']
    upload_image_after_hide = config.configs['UPLOAD_IMAGE_AFTER_HIDE']
    port = config.configs['PORT']
    
    res = {"result":{"url":f'{req_protocol}://{dom_address}:{port}{upload_image_after_hide}{img_name}'}}
    return json.dumps(res)

# Saves the audio taken from the API request
def save_audio_from_api(audio_url):
    response = requests.get(audio_url)

    audio_newreq_audio = '.' + config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + uuid.uuid4().hex + '.wav'
    with open(audio_newreq_audio, 'wb') as file:
        file.write(response.content)

    audio = AudioSegment.from_file(audio_newreq_audio)

    audio_name = uuid.uuid4().hex + '.wav'
    wav_output_path = '.' + config.configs["UPLOAD_SOUND_AFTER_HIDE"] + audio_name
    # Save Audio
    audio.export(wav_output_path , format='wav')

    req_protocol = config.configs['REQUEST_PROTOCOL']
    dom_address = config.configs['DOMAIN_ADDRESS']
    port = config.configs['PORT']
    upload_audio_after_hide = config.configs['UPLOAD_SOUND_AFTER_HIDE']
    
    res = {"result":{"url":f'{req_protocol}://{dom_address}:{port}{upload_audio_after_hide}{audio_name}'}}
    return json.dumps(res)



def get_route_reqs_status(user_id , type):
    res_queue = db.db.resQueue(user_id, type) # Get requests that are in queue
    res_processing = db.db.resProcessing(user_id, type) # Get requests that are processing
    
    res = api.get_res_from_api(res_queue,res_processing) # Get result of the requests that are not done
    
    for i in res:
        try:
            if json.loads(res[i][0])['result']['url'].split('.')[-1] == 'png':
                url = save_image_from_api(json.loads(res[i][0])['result']['url'])
            elif json.loads(res[i][0])['result']['url'].split('.')[-1] == 'wav':
                url = save_audio_from_api(json.loads(res[i][0])['result']['url'])
        except:
            url = res[i][0]
        finally:
            db.db.updateResFromApi(res[i][1], url, i)
    
    
    res_done = db.db.resDone(user_id, type) # Get requests that are done
    res_queue = db.db.resQueue(user_id, type) # Get requests that are in queue
    res_processing = db.db.resProcessing(user_id, type) # Get requests that are processing

    res = {'queue':res_queue, 'processing': res_processing, 'done': res_done}
    return res


def result_route_reqs_status(route):
    res = check_token()
    if res['status-code'] == 200:
        route_reqs_status = get_route_reqs_status(res["result"]["user_id"], route)
        res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
        return res
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
    
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            route_reqs_status = get_route_reqs_status(user_id, route)
            res = {'queue':route_reqs_status['queue'] , 'processing':route_reqs_status['processing'], 'done': route_reqs_status['done']}
            resp = make_response(res)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
            return resp
    abort (401)


# Retrieve request_id , status, params , result of steg audio
@app.route('/res-steg-audio' , methods =['POST'])
def res_steg_audio():
    res = result_route_reqs_status('/hide-text-in-sound')
    return res


# Retrieve request_id , status, params , result of extract steg audio
@app.route('/res-extr-steg-audio' , methods =['POST'])
def res_extr_steg_audio():
    res = result_route_reqs_status('/get-hidden-text-from-sound')
    return res


# Retrieve request_id , status, params, result, request uuid of stegano Image
@app.route('/get-all-img-res', methods = ['POST'])
def get_all_img_res():
    res = result_route_reqs_status('/hide-text-in-image')
    return res


# Retrieve request_id , status, params , result of extract image
@app.route('/res-extr-steg-img' , methods =['POST'])
def res_steg_image():
    res = result_route_reqs_status('/get-hidden-text-from-image')
    return res


# Retrieve request_id , status, params , result of add calc
@app.route('/get-all-add-req', methods = ['POST'])
def get_all_add_req():
    res = result_route_reqs_status('/add-two-numbers')
    return res


# Count route requests
def count_route_reqs(route1, route2):
    res = check_token()
    if res['status-code'] == 200:
        user_reqs_status = db.db.getAllReq(res["result"]["user_id"], route1, route2)
        try: 
            dict_result = {"count" : user_reqs_status[0][0]}
        except: 
            dict_result = {"count" : 0}
        j_result = json.dumps(dict_result)
        return j_result
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getAllReq(user_id, route1, route2)
            try: 
                dict_result = {"count" : user_reqs_status[0][0]}
            except: 
                dict_result = {"count" : 0}
            j_result = json.dumps(dict_result)
            resp = make_response(j_result)
            resp.set_cookie('access_token', s_token,max_age = 60 * 60)
            return resp
    abort (401)



# Returns count and status
@app.route('/res-add-calc' , methods=["POST"])
def res_add_calc():
    res = count_route_reqs('/add-two-numbers', None)
    return res


# Returns count and status
@app.route('/get-all-img-steg-req' , methods=['POST'])
def get_all_img_steg_req():
    res = count_route_reqs('/hide-text-in-image', '/get-hidden-text-from-image')
    return res


# Returns count and status
@app.route('/get-all-audio-steg-req', methods = ['POST'])
def get_all_audio_steg_req():
    res = count_route_reqs('/hide-text-in-sound', '/get-hidden-text-from-sound')
    return res


@app.route('/get-user-requests-status', methods=['POST'])
def get_user_requests_status():
    res = check_token()    
    if res['status-code'] == 200:
        user_reqs_status = db.db.getUserRequestsStatus(res["result"]["user_id"])
        dict_result = {"done":0 , "in queue":0 , "processing":0}
        
        for i in user_reqs_status:
            dict_result[i[0]] = i[1]
        j_result = json.dumps(dict_result)
        return j_result
    
    elif res['result'] == 'ExpiredToken':
        if session['logged_in'] is True:
            
            o_token = Token(username=session['username'])
            s_token = o_token.encode_token()
            user_id = db.db.getUserId(session['username'])
    
            user_reqs_status = db.db.getUserRequestsStatus(user_id)
            dict_result = {"done":0 , "in queue":0 , "processing":0}
            for i in user_reqs_status:
                dict_result[i[0]] = i[1]
            j_result = json.dumps(dict_result)
            
            resp = make_response(j_result)
            resp.set_cookie('access_token', s_token,max_age= 60 * 60)
    
            return resp
    abort (401)
    

@app.route('/get-size', methods=['POST'])
def get_size():    
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
        res = process.result(res["result"]["request_id"] , res["result"]["user_id"])
    return res


# Signup user
@app.route('/signup', methods=['POST'])
def signup():
    # Retrieve data from the body and header
    body_data = request.get_json()
    # header_data = request.headers
    
    o_user = User(body_data['username'] , body_data['email'] , body_data['password'])
    user = o_user.signup()
    
    if user["status"] == "True":
        res = {"result":{"confirm_link":user} , "status-code":201 }
    else:
        res = {"result":user["result"] , "status-code":400}
    return res


# To accept the link confirmation request
@app.route('/confirm', methods=['GET','POST'])
def _check_confirm():
    res = Email.check_confirm_email()
    if res['status'] == 'True':
        if res['api_req'] :
            result = {"result":"Email confirmed successfully", "status-code":200}
            return result
        return render_template('confirm_email.html')
    
    if res['api_req'] :
        result = {"result":"Confirmation email is not valid", "status-code":404}
        return result
    abort(404)


# Signin user
@app.route('/signin' ,methods=['POST'])
def signin():
    
    j_body_data = request.get_json()
    s_username = j_body_data['username']
    s_password = j_body_data['password']
    if s_username == 'admin' and s_password == 'admin':
        session['admin'] = True
        return admin.get_dashboard_info()
    o_user = User(username = s_username , password = s_password)
    o_user = o_user.signin()
    
    if o_user == 'True':        
        session['username'] = s_username
        session['logged_in'] = True
                
        # Set cookie : access token 
        o_token = Token(username=s_username)
        s_token = o_token.encode_token()
        res = {"result":{"token":s_token} , "status-code":200}        
        resp = make_response(res)
        resp.set_cookie('access_token', s_token,max_age= 60 * 60)            

    elif o_user == 'noactive' :
        resp = {"result":'your account is not active' , "status-code":403}        
    elif o_user == 'invalid':
        resp = {"result":o_user , "status-code":400}
    return resp


@app.route('/add-two-numbers', methods=['POST'])
def add():
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
    return res


@app.route('/hide-text-in-image', methods=['POST'])
def hide_text():
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
    return res


@app.route('/get-hidden-text-from-image', methods=['POST'])
def get_text():
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
    return res


@app.route('/get-result' , methods=['POST'])
def get_result():
    # Get request id
    s_req_id = request.get_json()["request_id"]    
    
    # Get Token
    try:
        s_token = request.headers.get('Authorization').split()[1]
    except:
        s_token = request.headers.get('Authorization')
    
    # Get id
    result = Token(token=s_token).handle_token()
    try:        
        # Token is valid
        user_id = int(result)                
        res = process.result(s_req_id,user_id)
        return res
    except:
        # Token is invalid.        
        res = {"result":result , "status-code":401}   
        return res   



@app.route('/hide-text-in-sound' , methods=['POST'])
def hide_in_sound():
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
    return res


@app.route('/get-hidden-text-from-sound' , methods=['POST'])
def get_from_sound():
    res = check_token_and_add_req_to_db()
    if res["status-code"] == 200:
        send_request.send(res["result"]["request_id"])        # Send request to queue
    return res


def add_to_db(user_id):    
    type = request.path # ex: /add
    
    if type == '/hide-text-in-image':   
        # Save image        
        try:
            img_steg_new_req_img = request.files['img_steg_new_req_img']         
            msg_steg_newreq_img = request.form['msg_steg_newreq_img']       
        except:
            info = request.get_json()
            msg_steg_newreq_img = info["params"]["text"]
            # Get image from URL
            image_url = info["params"]["url"]
            
            response = requests.get(image_url)
            img_steg_new_req_img = Image.open(BytesIO(response.content))
            response.raise_for_status()

        name_uuid = uuid.uuid4().hex
        img_src = name_uuid + '.png'
        img_path = '.' + config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src
        img_steg_new_req_img.save(img_path)        
        params = {"url" : config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src , 
                  "text" : msg_steg_newreq_img}
        
    elif type == '/get-hidden-text-from-image':
        try:
            extr_steg_img = request.files['extr_steg_img']
        except:
            # Get image from URL
            image_url = request.get_json()["params"]["url"]
            response = requests.get(image_url)
            extr_steg_img = Image.open(BytesIO(response.content))
            response.raise_for_status()

        name_uuid = uuid.uuid4().hex
        img_src = name_uuid + '.png'
        img_path = '.' + config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src
        extr_steg_img.save(img_path)
        params = {"url" : config.configs["UPLOAD_IMAGE_BEFORE_HIDE"] + img_src }

    elif type == '/get-hidden-text-from-sound':
        try:
            extr_steg_audio = request.files['extr_steg_audio']
        except:
            url = request.get_json()["params"]["url"]
            response = requests.get(url)
            extr_steg_audio = BytesIO(response.content)
            
        audio_name = uuid.uuid4().hex + '.wav'
        wav_output_path = '.' + config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + audio_name
        audio = AudioSegment.from_file(extr_steg_audio)
        audio.export(wav_output_path , format='wav')
        params = {"url" : config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + audio_name}
        
    elif type == '/hide-text-in-sound':
        try:
            msg_newreq_audio = request.form['msg_newreq_audio']
            audio_newreq_audio = request.files['audio_newreq_audio']
        except:
            msg_newreq_audio = request.get_json()["params"]["text"]
            url = request.get_json()["params"]["url"]
            response = requests.get(url)
            
            audio_newreq_audio = '.' + config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + uuid.uuid4().hex + '.wav'
            with open(audio_newreq_audio, 'wb') as file:
                file.write(response.content)

        audio = AudioSegment.from_file(audio_newreq_audio)
        
        # Save Audio
        audio_name = uuid.uuid4().hex + '.wav'
        wav_output_path = '.' + config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + audio_name
        audio.export(wav_output_path , format='wav')

        params = {"url" : config.configs["UPLOAD_SOUND_BEFORE_HIDE"] + audio_name ,
                  "text" : msg_newreq_audio}
        
    else:
        try:
            params = request.get_json()["params"]
        except:            
            params = {"params":"None"}
            
    j_params = json.dumps(params)
    agent = request.headers['User-Agent']
    method = request.method
    ip =  request.remote_addr
    time = str(datetime.now()) 
    
    req_id = db.db.addReqToDb(user_id, type, j_params, time, agent, method, ip, uuid.uuid4().hex)
    return str(req_id)


if __name__ == '__main__':
    time.sleep(10)
    t = threading.Thread(None, get_request.get_requests_from_queue, None, ())
    t.start()
    app.run(host=config.configs['HOST'], port=config.configs['PORT'] , debug=config.configs['DEBUG'])