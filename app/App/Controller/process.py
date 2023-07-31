from App.Controller import db_postgres_controller as db
from App.Controller.api_controller import api
import json
import os
from App import config

def process(req_id):
    db.db.updateInRequest(req_id, 0 ,'processing')
    
    # Get route and params
    req_info = db.db.getReqInfo(req_id)
    
    route = req_info[0][2]
    if route == '/add-two-numbers':
        result = add(req_info[0])
    elif route == '/hide-text-in-image':
        result = hide_text(req_info[0])
    elif route == '/get-hidden-text-from-image':        
        result = get_text(req_info[0])
    elif route == '/get-size':
        result = get_size(req_info[0])
    elif route == '/hide-text-in-sound':
        result = hide_in_sound(req_info[0])
    elif route == '/get-hidden-text-from-sound':
        result = get_from_sound(req_info[0])
    
    db.db.updateInRequest(req_id, result['request_id'], result['result'])
    return 'true'


def get_size(info):
    images_folder = config.configs["UPLOAD_IMAGE_AFTER_HIDE"]
    imgs_name = db.db.getImagesName(info[0])
    total_size = 0
    
    for file_dir in imgs_name:
        filename = file_dir[0]["result"]["url"].split('/')[-1]
        file_path = os.path.join(images_folder, filename)
        total_size += os.path.getsize(file_path)
        
    res = {"result":{"total_size":total_size}}
    
    res = json.dumps(res)
    return res


def add(info):
    res = api.add_two_numbers(int(info[3]["num1"]) , int(info[3]["num2"]))
    return res


def hide_text(info):
    text = info[3]["text"]
    image_path = info[3]["url"]
    res = api.hide_text_in_image(text, image_path)
    return res

def get_text(info):
    image_path = info[3]["url"]
    res = api.get_hidden_text_from_image(image_path)
    return res


def hide_in_sound(info):     
    text_to_hide = info[3]["text"]    
    audio_path = info[3]["url"]
    res = api.hide_audio_in_image(text_to_hide, audio_path)
    return res

def get_from_sound(info): 
    url = info[3]["url"]
    res = api.get_hidden_text_from_sound(url)
    return res
    
    
def result(s_req_id,user_id):
    # Get request process result if there is in process table
    res = db.db.getReqRes(user_id, s_req_id)
    
    if res == []:
        # There is no the processed request in process table
        
        # Now , check is there in request table or not
        res = db.db.checkIsInReqTB(user_id, s_req_id)
        
        if res == []:
            # There is no the request in request table
            res = {"result":"request id is wrong" , "status-code":400}
        else:
            res = {"result":"request is in queue" , "request_id":res[0][0] , "status-code":202}
        return res
    
    elif res[0][0] is None or res[0][1] != 'done' :
        # request accepted but not processed yet 
        res = {"result":"processing" , "request_id":s_req_id , "status-code":202}
        return res

    # There is process in process db table
    res = {"result":res[0][0]["result"] , "status-code":200 , "request_id":s_req_id}
    
    return res