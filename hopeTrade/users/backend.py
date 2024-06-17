from datetime import datetime
from django.contrib.auth import get_user_model
from .models import User
from django.core.mail import EmailMessage
from hopeTrade import settings
from datetime import datetime, time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from hopeTrade.settings import EMAIL_HOST_USER  # Asegúrate de tener una variable EMAIL_FROM en tus settings



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
    
def send_email(site_id, email):
    subject = "Sub"
    from_email, to = EMAIL_HOST_USER, email
    text_content = 'Text'
    html_content = render_to_string(
        'app/includes/email.html',
        {'pk': site_id}
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def diaValido(date):
    today = datetime.now().date()
    if date <= today:
        return False, "La fecha debe ser mayor al día de hoy."
    if date.weekday() >= 5:  # 5 y 6 son sábado y domingo
        return False, "La fecha debe ser un día entre lunes y viernes."
    return True, ""
        
    
def clean_hour(unaHora):
    if not (time(8, 0) <= unaHora <= time(20, 0)):
        return False, "La hora debe estar entre las 8 y las 20 hs."
    return True, ""