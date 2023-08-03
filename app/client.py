import requests
import threading
import argparse

parser = argparse.ArgumentParser()

def add_argument_parser():
    arguments = [
        ['--route', 'route -> ex: /add-two-numbers'],
        ['--num1', 'first number'],
        ['--num2', 'second number'],
        ['--reqid', 'your request id'],
        ['--token', 'token (JWT)'],
        ['--username', 'your username'],
        ['--password', 'your password'],
        ['--confirm_link', 'confirm link'],
        ['--email', 'your email'],
        ['--size', 'requests size'],
        ['--address', 'Domain Address'],
        ['--url', 'your image url'],
        ['--text', 'your text to hide in image '],
        ['--path', 'Your image path '],
    ]
    
    # ex: '--text', 'your text to hide in image '
    for arg,help in arguments:
      parser.add_argument(arg, help=help)  
    return


def send_request(url, data, headers):
    response = requests.post(url, json=data, headers=headers)
    print(response.text)


def send_multiple_requests(data, size, route, address, headers=None):
    url = '%s/%s' % (address, route)
    
    for _ in range(size):
        t = threading.Thread(target=send_request, args=(url, data, headers))
        t.start()


# add
def add_two_numbers_route(req_size,address):
    args = parser.parse_args()
    data = {"params":{"num1": int(args.num1), "num2": int(args.num2)}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'add-two-numbers', address, headers)
    
        
# get result    
def get_result_route(req_size, address):
    args = parser.parse_args()
    data = {"request_id":args.reqid}
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-result', address, headers)
    
# sign in
def signin_route(req_size, address):
    args = parser.parse_args()
    data = {"username": args.username,"password": args.password}
    send_multiple_requests(data, req_size, 'signin', address) 

# confirm link
def confirm_route(req_size, address):
    args = parser.parse_args()
    data = {"confirm_link": args.confirm_link}
    send_multiple_requests(data, req_size, 'confirm', address)

# sign up
def signup_route(req_size, address):
    args = parser.parse_args()
    data = {"username": args.username,"password": args.password,"email": args.email}
    send_multiple_requests(data, req_size, 'signup', address)

# hide text
def hide_text(req_size, address):
    args = parser.parse_args()
    data = {"params":{"url": args.url, "path":args.path , "text": args.text}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'hide-text-in-image', address, headers)    

# get text
def get_text(req_size, address):
    args = parser.parse_args()
    data = {"params":{"url": args.url , "path":args.path}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-hidden-text-from-image', address, headers)    
    
# hide text message in sound
def hide_in_sound(req_size, address):
    args = parser.parse_args()
    data = {"params":{"url": args.url , "path":args.path , "text": args.text}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'hide-text-in-sound', address, headers)    


# get text message from sound
def get_from_sound(req_size, address):
    args = parser.parse_args()
    data = {"params":{"url": args.url , "path":args.path}} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-hidden-text-from-sound', address, headers)    
    
    
# get size
def get_size(req_size, address):
    args = parser.parse_args()
    data = {} 
    headers = {'Authorization': args.token}
    send_multiple_requests(data, req_size, 'get-size', address, headers)    
    
    
def main():
    add_argument_parser()
    
    address = parser.parse_args().address
    route = parser.parse_args().route
    try:
        req_size = int(parser.parse_args().size)
    except:
        req_size = 1
        
    if req_size is None or req_size < 1 :
        req_size = 1
    
    if route == 'add-two-numbers' :
        add_two_numbers_route(req_size, address)
        
    elif route == 'get-result' :
        get_result_route(req_size, address)
    
    elif route == 'signin':
        signin_route(req_size, address)
    
    elif route == 'confirm':
        confirm_route(req_size, address)
        
    elif route == 'signup':
        signup_route(req_size, address)
        
    elif route == 'hide-text-in-image':
        hide_text(req_size, address)
    
    elif route == 'get-hidden-text-from-image':
        get_text(req_size, address)
        
    elif route == 'get-size':
        get_size(req_size, address)
        
    elif route == 'hide-text-in-sound':
        hide_in_sound(req_size, address)
        
    elif route == 'get-hidden-text-from-sound':
        get_from_sound(req_size, address)
        
    else:
        print("Invalid Route")
        
main()