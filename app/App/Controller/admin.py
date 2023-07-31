import json
from App.Controller import db_postgres_controller as db
from flask import request

def get_dashboard_info():
    users_reqs_status = db.db.admin_getUsersRequestsStatus()
    dict_result = {"status-code":200, "result": {"done":0 , "in queue":0 , "processing":0}}
    for i in users_reqs_status:
        dict_result["result"][i[0]] = i[1]
    
    dict_result["result"]["all_add_reqs"] = db.db.admin_getAllReq('/add-two-numbers', None)[0][0]
    dict_result["result"]["all_img_steg_reqs"] = db.db.admin_getAllReq('/hide-text-in-image', '/get-hidden-text-from-image')[0][0]
    dict_result["result"]["all_audio_steg_reqs"] = db.db.admin_getAllReq('/hide-text-in-sound', '/get-hidden-text-from-sound')[0][0]

    j_result = json.dumps(dict_result) 
    return j_result

# Takes a route and returns all successful, processing and in queue requests
def get_route_reqs_status(type):
    res_done = db.db.admin_resDone(type)
    res_queue = db.db.admin_resQueue(type)
    res_processing = db.db.admin_resProcessing(type)
    res = {'queue':res_queue, 'processing': res_processing, 'done': res_done}
    return res

def res_add_calc():
    users_add_req_status = get_route_reqs_status('/add-two-numbers')
    result = {"status-code":200 , "result":users_add_req_status}
    j_result = json.dumps(result)
    return j_result 
    
def res_steg_img():
    users_steg_img_req_status = get_route_reqs_status('/hide-text-in-image')
    result = {"status-code":200 , "result":users_steg_img_req_status}
    j_result = json.dumps(result)
    return j_result

def res_extr_steg_img():
    users_extr_steg_img_req_status = get_route_reqs_status('/get-hidden-text-from-image')
    result = {"status-code":200 , "result":users_extr_steg_img_req_status}
    j_result = json.dumps(result)
    return j_result
 
def res_steg_audio():
    users_steg_audio_req_status = get_route_reqs_status('/hide-text-in-sound')
    result = {"status-code":200 , "result":users_steg_audio_req_status}
    j_result = json.dumps(result)
    return j_result

def res_extr_audio():
    users_extr_steg_audio_req_status = get_route_reqs_status('/get-hidden-text-from-sound')
    result = {"status-code":200 , "result":users_extr_steg_audio_req_status}
    j_result = json.dumps(result)
    return j_result


# users info
def users_info():
    users_info = db.db.admin_get_users_info()
    result = {"status-code":200 , "result":users_info}
    j_result = json.dumps(result)
    return j_result