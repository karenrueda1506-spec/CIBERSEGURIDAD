# database/init_db.py
from database.db_connection import DatabaseConnection

def initialize_database():
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create roles table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                salt VARCHAR(32) NOT NULL,
                role_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles(id)
            )
            """)
            
            # Create interactions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # Insert default roles
            cursor.execute("""
            INSERT IGNORE INTO roles (id, name, description) VALUES
            (1, 'superadmin', 'Superadministrador con acceso completo al sistema'),
            (2, 'teacher', 'Docente/Gestor que puede cargar material educativo'),
            (3, 'student', 'Estudiante que interactúa con el chatbot')
            """)
            
            # Insert default superadmin user (password: Admin123)
            cursor.execute("""
            INSERT IGNORE INTO users (username, email, password_hash, salt, role_id) VALUES
            ('superadmin', 'admin@cybersecurity.edu', 
             '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
             'salt_superadmin_123', 1)
            """)
            
            connection.commit()
            print("✅ Base de datos inicializada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("❌ No se pudo conectar a la base de datos")

if __name__ == "__main__":
    initialize_database()