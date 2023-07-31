import hashlib
import re 
import Levenshtein
from App.Controller.email_controller import Email
from App.Controller import db_postgres_controller as db

class Valid:
    
    def __init__(self, username=None, email=None, password=None):
        self.username = username        
        self.email = email
        self.password = password
            
        
    # Check email is valid or not
    def is_valid_email(self):
        if not self.email :
            return "empty_email" # Email is empty
        
        # Check duplicate email
        check_exist_email = Email.is_exist_email(self.email)
        if check_exist_email is None :
            pass
        elif check_exist_email == True :
            return "duplicate_email"
        elif check_exist_email == "noactive":
            return "noactive"
            
        
        if len(self.email) > 320:
            return "email_length" # Email length must be less than 100 chars
        
        sim = self.calculate_similarity(self.email.split('@')[0] , self.password)
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, self.email):
            if sim >= 75 :
                return "used_info_in_password"
            else:
                return "True"
        else:
            return "char_email" # Email chars is not valid
        


    # Check username is valid or not
    def is_valid_username(self):
        if not self.username :
            return "empty_username" # username is empty
        # Check duplicate username
        check_exist_username = db.db.checkDuplicateUsername(self.username)
        
        if check_exist_username == "True":
            return "duplicate_username"
        if len(self.username) > 30 or len(self.username) < 3:
            return "length_username"  # username length is must be less than 30 letters
        
        username_allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._0123456789")
        if not set(self.username).issubset(username_allowed_chars):
            return "char_username" # username chars is not valid
        return "True"
    
    
    # Check password is valid or not
    def is_valid_password(self):
        if not self.password :
            return "empty_password"
        
        pass_pattern1 = re.compile(r".{8,50}") # The password must be between 8 and 50 characters long
        pass_pattern2 = re.compile(r"[A-Za-z]+") # The password must have english letter(s)
        pass_pattern3 = re.compile(r"\d+") # The password must have number(s)
        pass_pattern4 = re.compile(r"[!@#$%^&*()<>?/\|}{~:]") # The password must have special character(s)
        
        sim = self.calculate_similarity(self.username , self.password)
        if pass_pattern2.search(self.password) is None or pass_pattern3.search(self.password) is None or pass_pattern4.search(self.password) is None :
            return "char_password"
        elif pass_pattern1.fullmatch(self.password) is None:
            return "password_length"
        elif sim >= 75:
            return "used_info_in_password"
        return "True"
    
    
    
    def check_match_info(self):
        # Get users info
        hash_password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        l_user_info = db.db.checkSigninInfo(self.username,hash_password)

        # i[0] is username and i[1] is password and i[2] is active column
        if l_user_info is not None:
            if l_user_info[2] == True: 
                return "True"  
            return "noactive"
        return "invalid" # Invalid username or password

    # check whether the username and password are valid
    def signin(self):        
        check_match_info = self.check_match_info()    
        return check_match_info
        

    # It checks whether the signup info are valid
    def signup(self):    
        
        check_valid_username = self.is_valid_username()
        if check_valid_username != "True":
            return check_valid_username
        
        check_valid_password = self.is_valid_password()
        if check_valid_password != "True":
            return check_valid_password

        check_valid_email = self.is_valid_email()
        return check_valid_email        
        
    
    
    # Used Levenshtein distance to calculate similarity between two strings
    def calculate_similarity(self,string1, string2):
        distance = Levenshtein.distance(string1, string2)
        max_length = max(len(string1), len(string2))
        
        similarity = 1 - (distance / max_length)
        return similarity * 100
