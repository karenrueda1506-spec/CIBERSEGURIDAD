# app/views/student_view.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.whatever.openai_agent import OpenAIAgent
from app.models.interaction_model import InteractionModel

student_bp = Blueprint('student', __name__)
ai_agent = OpenAIAgent()
interaction_model = InteractionModel()

@student_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('student/dashboard.html')

@student_bp.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    user_message = request.json.get('message')
    user_id = session['user_id']
    
    if not user_message:
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    try:
        # Get response from OpenAI (sin API Key por ahora)
        bot_response = ai_agent.get_response(user_message, "student")
        
        # Save interaction to database
        interaction_model.save_interaction(user_id, user_message, bot_response)
        
        return jsonify({'response': bot_response})
    
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500