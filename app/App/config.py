import os
from dotenv import load_dotenv
load_dotenv()

configs = {
    
    'SYSTEM_NAME' : os.getenv('SYSTEM_NAME') , 
    'DOMAIN_ADDRESS' : os.getenv('DOMAIN_ADDRESS') ,
    
    'TARGET_API_URL' : os.getenv('TARGET_API_URL') ,
    
    'HOST' : os.getenv('HOST') , 
    'PORT' : os.getenv('PORT') , 
    'DEBUG' : os.getenv('DEBUG') , 
    'SECRET_KEY' : os.getenv('SECRET_KEY') ,
    'SEND_FILE_MAX_AGE_DEFAULT' : os.getenv('SEND_FILE_MAX_AGE_DEFAULT') ,
    
    # API Info
    'API_USERNAME' : os.getenv('API_USERNAME') ,
    'API_PASSWORD' : os.getenv('API_PASSWORD') ,
    
    # Database 
    'DB_NAME' : os.getenv('DB_NAME') ,
    'DB_HOST' : os.getenv('DB_HOST') ,
    'DB_USER' : os.getenv('DB_USER') ,
    'DB_PASSWORD' : os.getenv('DB_PASSWORD') ,
    'DB_PORT' : os.getenv('DB_PORT') ,
    
    # JWT
    'JWT_SECRET_KEY' : os.getenv('JWT_SECRET_KEY') ,
    
    # Email
    'SMTP_SERVER' : os.getenv('SMTP_SERVER') ,
    'SMTP_PORT' : os.getenv('SMTP_PORT') ,
    'SENDER_EMAIL' : os.getenv('SENDER_EMAIL') ,
    'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD') ,
    'EMAIL_SUBJECT' : os.getenv('EMAIL_SUBJECT') ,
    
    # Images
    'UPLOAD_IMAGE_BEFORE_HIDE' : os.getenv('UPLOAD_IMAGE_BEFORE_HIDE') ,
    'UPLOAD_IMAGE_AFTER_HIDE' : os.getenv('UPLOAD_IMAGE_AFTER_HIDE') ,
    
    # Sounds
    'UPLOAD_SOUND_BEFORE_HIDE' : os.getenv('UPLOAD_SOUND_BEFORE_HIDE') ,
    'UPLOAD_SOUND_AFTER_HIDE' : os.getenv('UPLOAD_SOUND_AFTER_HIDE') ,
    
    # Docker Compose
    'RABBITMQ_SERVICE_NAME': os.getenv('RABBITMQ_SERVICE_NAME') , 
}