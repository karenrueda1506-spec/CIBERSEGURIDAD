# app/models/user_model.py
from database.db_connection import DatabaseConnection
import hashlib
import secrets
import re

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def validate_email(self, email):
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def user_exists(self, username, email):
        """Verificar si usuario o email ya existen"""
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error checking user existence: {e}")
                return True
            finally:
                cursor.close()
                connection.close()
        return True
    
    def create_user(self, username, email, password, role_id):
        """Crear usuario con validaciones"""
        # Validaciones
        if not self.validate_email(email):
            raise ValueError("Formato de email inválido")
        
        if self.user_exists(username, email):
            raise ValueError("El usuario o email ya existen")
        
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Hash password
                salt = secrets.token_hex(16)
                hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
                password_hash = hashed_password.hex()
                
                query = """
                INSERT INTO users (username, email, password_hash, salt, role_id, created_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(query, (username, email, password_hash, salt, role_id))
                connection.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error creating user: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
    
    def authenticate_user(self, email, password):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                
                if user:
                    # Verify password
                    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user['salt'].encode('utf-8'), 100000)
                    if hashed_password.hex() == user['password_hash']:
                        return user
                return None
            except Exception as e:
                print(f"Error authenticating user: {e}")
                return None
            finally:
                cursor.close()
                connection.close()