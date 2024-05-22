from datetime import datetime
from django.contrib.auth import get_user_model
from .models import User
from django.core.mail import EmailMessage
from hopeTrade import settings

def calculate_califications():
    return 1.0

def authenticate(request, dni=None, password=None, **kwargs):
    UserModel = get_user_model()
    try:
        usuario = User.objects.get(dni=dni)
        if usuario.password == password:
            return usuario
    except User.DoesNotExist:
        return None

def get_years(date):
    actual_date = datetime.now().date()
    edad = actual_date.year - date.year - \
        ((actual_date.month, actual_date.day) < (date.month, date.day))
    return edad

def enviarMail(mail, asunto, cuerpo):
    try:
        email = EmailMessage(
        asunto,
        cuerpo,
        settings.EMAIL_HOST_USER,
        [mail],
        )
        email.send(fail_silently=False)
        return True
    except Exception as e:
        # Imprime la excepción para depuración
        print(f"Error al enviar el correo: {e}")
        return False