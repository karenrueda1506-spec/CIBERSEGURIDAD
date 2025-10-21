# app/whatever/openai_agent.py
from app.config import config

class OpenAIAgent:
    def __init__(self):
        self.context = """
        Eres un asistente educativo especializado en ciberseguridad. 
        Responde preguntas sobre: contraseñas seguras, phishing, redes sociales, protección de datos.
        """
    
    def get_response(self, user_message, user_role="student", conversation_history=None):
        # Sin API Key - Respuestas predefinidas
        responses = {
            "contraseña": """
**¿Qué es una contraseña segura?**

Una contraseña segura debe tener:
- Mínimo 12 caracteres
- Mayúsculas, minúsculas, números y símbolos
- No usar información personal
- Ejemplo: `M1_C0ntr@s3ñ4_S3gur4!`

**Consejos:**
- Usa un gestor de contraseñas
- No reutilices contraseñas
- Activa autenticación de dos factores
""",
            "phishing": """
**¿Cómo identificar phishing?**

🔴 Señales de alerta:
- Remitente sospechoso
- Urgencia artificial ("Tu cuenta será cerrada")
- Errores gramaticales
- Enlaces que no coinciden

✅ Buenas prácticas:
- Verifica la URL antes de hacer clic
- No descargues archivos sospechosos
- Contacta a la empresa directamente
""",
            "autenticación de dos factores": """
**¿Qué es la autenticación de dos factores (2FA)?**

Es una capa adicional de seguridad que requiere:

1. **Algo que sabes** - Tu contraseña
2. **Algo que tienes** - Código en tu teléfono

**Ejemplos:**
- Códigos SMS
- Google Authenticator
- Notificaciones push
- Llaves de seguridad física

**¿Por qué es importante?**
- Previene el 99.9% de ataques
- Protege incluso si tu contraseña es robada
"""
        }
        
        # Buscar respuesta predefinida
        user_message_lower = user_message.lower()
        
        for key, response in responses.items():
            if key in user_message_lower:
                return response
        
        # Respuesta por defecto
        return """
🤖 **Asistente de Ciberseguridad**

Parece que hay un problema temporal con mi conexión. Mientras se soluciona, puedo ayudarte con:

🔒 **Contraseñas seguras** - Cómo crear y gestionar contraseñas robustas
🎣 **Detección de phishing** - Identificar correos y mensajes fraudulentos  
⚡ **Autenticación de dos factores** - Capa adicional de seguridad
📱 **Seguridad en redes sociales** - Proteger tu información personal

Por favor, intenta tu pregunta de nuevo especificando uno de estos temas.
"""