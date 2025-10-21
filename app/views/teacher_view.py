# app/views/teacher_view.py
from flask import Blueprint, render_template, session, redirect, url_for

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role_id') != 2:
        return redirect(url_for('auth.login'))
    return render_template('teacher/dashboard.html')