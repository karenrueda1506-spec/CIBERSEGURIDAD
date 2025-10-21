# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI - Sin API Key por ahora
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_desarrollo')
    
    # Database
    DB_HOST = os.getenv('DB_HOST', "bxxexopbdx6uayizd2xz-mysql.services.clever-cloud.com")
    DB_NAME = os.getenv('DB_NAME', "bxxexopbdx6uayizd2xz")
    DB_USER = os.getenv('DB_USER', "u107jzojitvr7eow")
    DB_PASSWORD = os.getenv('DB_PASSWORD', "G8Mk7aWXctMkxBtBZQ1J")
    DB_PORT = int(os.getenv('DB_PORT', '3306'))

config = Config()
