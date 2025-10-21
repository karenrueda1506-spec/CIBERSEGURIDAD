# app/views/admin_view.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from app.models.user_model import UserModel
from database.db_connection import DatabaseConnection
import os

admin_bp = Blueprint('admin', __name__)
user_model = UserModel()

@admin_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    stats = get_system_stats()
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
def list_users():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    users = get_all_users()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        
        user_id = user_model.create_user(username, email, password, role_id)
        if user_id:
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('admin.list_users'))
        else:
            flash('Error al crear usuario', 'error')
    
    return render_template('admin/create_user.html')

@admin_bp.route('/metrics')
def view_metrics():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    metrics = get_system_metrics()
    return render_template('admin/metrics.html', metrics=metrics)

@admin_bp.route('/roles')
def manage_roles():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    roles = get_all_roles()
    return render_template('admin/roles.html', roles=roles)

@admin_bp.route('/system')
def system_config():
    if 'user_id' not in session or session.get('role_id') != 1:
        return redirect(url_for('auth.login'))
    
    config_data = get_system_config()
    return render_template('admin/system_config.html', config=config_data)

# Funciones auxiliares (las que ya te había dado)
def get_system_stats():
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']
            
            cursor.execute("SELECT COUNT(*) as today FROM interactions WHERE DATE(timestamp) = CURDATE()")
            today_interactions = cursor.fetchone()['today']
            
            cursor.execute("SELECT COUNT(DISTINCT user_id) as active FROM interactions WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY) AND user_id IN (SELECT id FROM users WHERE role_id = 3)")
            active_students = cursor.fetchone()['active']
            
            return {
                'total_users': total_users,
                'today_interactions': today_interactions,
                'active_students': active_students
            }
        except Exception as e:
            return {'total_users': 0, 'today_interactions': 0, 'active_students': 0}
        finally:
            cursor.close()
            connection.close()
    return {'total_users': 0, 'today_interactions': 0, 'active_students': 0}

def get_all_users():
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT u.id, u.username, u.email, u.created_at, r.name as role_name FROM users u JOIN roles r ON u.role_id = r.id ORDER BY u.created_at DESC")
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def get_system_metrics():
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT r.name as role, COUNT(u.id) as count FROM users u JOIN roles r ON u.role_id = r.id GROUP BY r.name")
            users_by_role = cursor.fetchall()
            
            cursor.execute("SELECT DATE(timestamp) as date, COUNT(*) as count FROM interactions WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY) GROUP BY DATE(timestamp) ORDER BY date DESC")
            interactions_by_day = cursor.fetchall()
            
            return {
                'users_by_role': users_by_role,
                'interactions_by_day': interactions_by_day
            }
        except Exception as e:
            return {'users_by_role': [], 'interactions_by_day': []}
        finally:
            cursor.close()
            connection.close()
    return {'users_by_role': [], 'interactions_by_day': []}

def get_all_roles():
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM roles ORDER BY id")
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def get_system_config():
    return {
        'openai_api_key': '••••••••••••' + (os.getenv('OPENAI_API_KEY', '')[-4:] if os.getenv('OPENAI_API_KEY') else ''),
        'max_users': 1000,
        'backup_frequency': 'daily',
        'session_timeout': 30,
        'chatbot_enabled': True
    }

def get_user_count_by_role(role_id):
    connection = DatabaseConnection().get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role_id = %s", (role_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0
        finally:
            cursor.close()
            connection.close()
    return 0