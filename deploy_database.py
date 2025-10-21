from database.db_connection import DatabaseConnection
import os

def deploy_database():
    db = DatabaseConnection()
    connection = db.get_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Leer y ejecutar el script SQL
            with open('database_schema.sql', 'r') as file:
                sql_script = file.read()
            
            # Ejecutar cada sentencia por separado
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            
            connection.commit()
            print("✅ Base de datos desplegada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error desplegando base de datos: {e}")
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    deploy_database()