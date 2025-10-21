# run.py
from flask import Flask, redirect
from app.views.auth_view import auth_bp
from app.views.admin_view import admin_bp
from app.views.teacher_view import teacher_bp
from app.views.student_view import student_bp
from database.init_db import initialize_database
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_desarrollo')

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(teacher_bp, url_prefix='/teacher')
app.register_blueprint(student_bp, url_prefix='/student')

@app.route('/')
def index():
    return redirect('/login')

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'chatbot-ciberseguridad'}

if __name__ == '__main__':
    # Initialize database
    print("🚀 Iniciando Chatbot de Ciberseguridad...")
    print("🔄 Inicializando base de datos...")
    initialize_database()
    
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    
    print(f"🌐 Servidor iniciando en: http://{host}:{port}")
    app.run(host=host, port=port, debug=True)