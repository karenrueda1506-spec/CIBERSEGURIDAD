# app/models/user_model.py
from database.db_connection import DatabaseConnection
import hashlib
import secrets

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_user(self, username, email, password, role_id):
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