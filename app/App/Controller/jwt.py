from App.Controller import db_postgres_controller as db
import jwt
import datetime
from App import config

class Token :
    
    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token
    
        # Set jwt secret key
        self.secret_key = config.configs['JWT_SECRET_KEY']
    
    
    def encode_token(self):         
        # Get the current datetime
        current_datetime = datetime.datetime.utcnow()
        # Add 2 days to the current datetime
        expiration_datetime = current_datetime + datetime.timedelta(minutes=10)
        # Calculate the corresponding Unix timestamp
        unix_timestamp = int(expiration_datetime.timestamp())
           
        # Define the payload (claims)
        payload = {            
            'username': self.username,
            'expiration_time' : unix_timestamp
        }

        # Define the header
        header = {
            'alg': 'HS256',
            'typ': 'JWT',
        }
        # Encode the JWT with custom header and payload
        s_token = jwt.encode(payload, self.secret_key, algorithm='HS256', headers=header)
        
        db.db.addTokenToDb(s_token, self.username,)
        return s_token
    
    
    def handle_token(self):
        decode_res = self.decode_token()
        
        if decode_res == 'WrongToken':
            return 'WrongToken'
        exp_time = decode_res['expiration_time']
        username = decode_res['username']
        
        current_datetime = datetime.datetime.utcnow().timestamp()
        if exp_time < current_datetime :
            return 'ExpiredToken'
        
        get_id = db.db.getUserId(username)
        return str(get_id[0])
        
        
    def decode_token(self):
        try:
            # Decode the JWT and get the payload and header
            payload = jwt.decode(self.token, self.secret_key, algorithms=['HS256'])
            return payload
            
        except jwt.DecodeError:
            return 'WrongToken'