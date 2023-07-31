from App.Controller.email_controller import Email
from App.Controller import db_postgres_controller as db
from App.Controller.validation import Valid
import hashlib

class User:

    def __init__(self,  username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password        
        
    # Do signup user
    def signup(self):        
        check_user_info = self.is_valid_signup()        

        if check_user_info == "True":
            # Send confirmation email
            email = Email()
            s_confirmation_link = email.send_confirmation_email(self.email, self.username)
            
            # To save password in database as hash.
            password = hashlib.md5(self.password.encode("utf-8")).hexdigest()
            db.db.signupUser(self.username, self.email, password, s_confirmation_link)

            res = {"status":"True", "link": s_confirmation_link}
            return res
        
        res = {"status":"False", "result": check_user_info}
        return res
        
    
    
    def is_valid_signup(self):
        # Validate signup info
        valid = Valid(username = self.username , email = self.email , password = self.password)
        valid_info = valid.signup()
        return valid_info
                                    

    # Do signin user
    def signin(self):        
        check_user_info = self.is_valid_signin()
        return check_user_info    
    
    # True if user password is True. noactive if user did signup but did not active
    def is_valid_signin(self):        
        valid = Valid(username=self.username, password=self.password)        
        valid_info = valid.signin()
        return valid_info
        