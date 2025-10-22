# app/views/auth_view.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)
user_model = UserModel()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = user_model.authenticate_user(email, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role_id'] = user['role_id']
            session['email'] = user['email']
            
            # Redirect based on role
            if user['role_id'] == 1:  # Superadministrador
                return redirect(url_for('admin.dashboard'))
            elif user['role_id'] == 2:  # Docente/Gestor
                return redirect(url_for('teacher.dashboard'))
            else:  # Estudiante
                return redirect(url_for('student.dashboard'))
        else:
            flash('Credenciales inválidas. Intenta nuevamente.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validaciones básicas
        if not username or not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/register.html')
        
        # Crear usuario automáticamente como ESTUDIANTE (role_id = 3)
        user_id = user_model.create_user(username, email, password, 3)  # 3 = Estudiante
        
        if user_id:
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al crear la cuenta. El email o usuario ya existe.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))