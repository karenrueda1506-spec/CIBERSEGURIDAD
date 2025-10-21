# app/models/interaction_model.py
from database.db_connection import DatabaseConnection

class InteractionModel:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def save_interaction(self, user_id, user_message, bot_response):
        connection = self.db.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO interactions (user_id, user_message, bot_response)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (user_id, user_message, bot_response))
                connection.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error saving interaction: {e}")
                return None
            finally:
                cursor.close()
                connection.close()