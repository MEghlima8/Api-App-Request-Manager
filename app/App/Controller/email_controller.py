from flask import request
from App.Controller import db_postgres_controller as db
import smtplib
import ssl
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from App import config


class Email:
    
    def  __init__(self):
        self.s_smtp_server = config.configs['SMTP_SERVER']
        self.i_port = int(config.configs['SMTP_PORT'])
        self.s_sender_email = config.configs['SENDER_EMAIL']
        self.s_password = config.configs['SMTP_PASSWORD']
        self.email_subject = config.configs['EMAIL_SUBJECT']

    def send_confirmation_email(self, email, username):

        # Verify link key
        s_link_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        
        t = threading.Thread(None, self.send_confirmation_link_multiThread, None, (email, username, s_link_key))
        t.start()
        
        return s_link_key
        
        
    def send_confirmation_link_multiThread(self, email, username, s_link_key ):
        domain_address = config.configs['DOMAIN_ADDRESS']
        port = config.configs['PORT']
        request_protocol = config.configs['REQUEST_PROTOCOL']
        system_name = config.configs['SYSTEM_NAME']
        # The link to which the confirmation request will be emailed
        s_link = '%s://%s:%s/confirm?link=%s' % (request_protocol, domain_address, port, s_link_key)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.email_subject
        msg['From'] = self.s_sender_email
        msg['To'] = email
        
        s_text = '''سلام {username} برای تایید حساب خود در سامانه {system_name} روی لینک زیر کلیک کنید در غیر این صورت این ایمیل را نادیده بگیرید.
        {link}
        '''.format(username=username, system_name=system_name ,link=s_link)
        
        s_text_mime = MIMEText(s_text, 'plain','utf-8')
        
        msg.attach(s_text_mime)
        

        # reference : https://www.mongard.ir/one_part/170/sending-email-python/
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.s_smtp_server, self.i_port, context=context) as server:
            server.login(self.s_sender_email, self.s_password) 
            server.sendmail(self.s_sender_email, email, msg.as_string())
            server.quit()
            
            return s_link_key
  
    

    @staticmethod
    def check_confirm_email():
        api_req = False
        try:
            body_data = request.get_json()
            s_link = body_data['confirm_link']
            api_req = True
        except:
            s_link = request.args.get('link')
        is_exist = db.db.getUserConfirmLink(s_link)
        
        if is_exist is not None :
            db.db.activeUser(s_link)
            res = {"status":'True', 'api_req': api_req}
            return res
        res = {"status":'False', 'api_req': api_req}
        # Confirm link is wrong
        return res
    

    @staticmethod
    def is_exist_email(email):        
        # Getback users info
        l_users_info = db.db.getActiveFromUsers(email)

        if l_users_info is None :    
            return False
        elif l_users_info[0] == True:            
            return True
        return 'noactive'
        
        