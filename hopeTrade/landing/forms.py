from django import forms
from .models import Publication
from hopeTrade.settings import STATIC_URL, BASE_DIR
import os
from datetime import date, datetime, time, timezone
from django.utils import timezone
from django.core.exceptions import ValidationError

def get_png_files():
    static_dir = os.path.join(BASE_DIR, "landing",STATIC_URL)
    png_files = [f for f in os.listdir(static_dir) if f.endswith('.png')]
    return [(f, f) for f in png_files]

class CreateNewPublication(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, widget=forms.TextInput())
    description = forms.CharField(label='Descripcion', max_length=500, widget=forms.TextInput())
    category = forms.ChoiceField(
        label='Categoria',
        choices=[
            ('alimento', 'Alimento'),
            ('limpieza', 'Limpieza'),
            ('higiene', 'Higiene'),
            ('electrodomestico', 'Electrodomestico'),
            ('jueguete', 'Juguetes')
        ],
        widget=forms.Select()
    )
    state = forms.ChoiceField(
        label='Estado del Producto',
        choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')],
        widget=forms.Select()
    )
    date = forms.DateField(
        label='Fecha de Vencimiento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    file = forms.ChoiceField(
        label='Nombre del archivo png',
        choices=get_png_files(),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        expiration_date = cleaned_data.get("date")

        if category == 'alimento':
            if not expiration_date:
                raise ValidationError("La fecha de vencimiento es obligatoria para la categoría 'Alimento'.")
            if expiration_date < date.today():
                raise ValidationError("La fecha de vencimiento no puede ser una fecha pasada.")
        else:
            cleaned_data['date'] = None  # Remove the date if the category is not 'Alimento'

        return cleaned_data
    
    
class EditPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ['user', 'file']
        widgets = {
            'category': forms.Select(choices=[('alimento', 'Alimento'), ('limpieza', 'Limpieza'), ('higiene', 'Higiene'), ('electrodomestico', 'Electrodomestico'), ('jueguete', 'Juguetes')]),
            'state': forms.Select(choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')]),
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CreateNewOffer(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, widget=forms.TextInput())
    date = forms.DateField(label='Fecha de Encuentro', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    hour = forms.TimeField(label='Hora', widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    sede = forms.ChoiceField(label='Sede', choices=[
        ('LA PLATA', 'La Plata'),
        ('BURZACO', 'Burzaco'),
        ('MORON', 'Moron'),
        ('VILLA ELISA', 'Villa Elisa'),
        ('LAS FLORES', 'Las Flores'),
        ('MERLO', 'Merlo')
    ], widget=forms.Select())
    description = forms.CharField(
        label='Descripción de la oferta',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 60})
    )

#   def clean_date(self):
#        date = self.cleaned_data['date']
#        if date.weekday() >= 5:  # 5 y 6 son sábado y domingo
#            raise ValidationError("La fecha debe ser un día entre lunes y viernes.")
#        if date < datetime.now().date():
#            raise ValidationError("La fecha no puede ser una fecha pasada.")
#       return date

    # CAMBIAR PARA QUE NO SE PUEDAN REALIZAR INTERCAMBIOS EN EL MIMSMO DIA DE LA FECHA
    def clean_date(self):
            date = self.cleaned_data['date']
            if date.weekday() >= 5:  # 5 y 6 son sábado y domingo
                raise ValidationError("La fecha debe ser un día entre lunes y viernes.")
            if date < datetime.now().date():
                raise ValidationError("La fecha no puede ser una fecha pasada.")
            return date

    def clean_hour(self):
        hour = self.cleaned_data['hour']
        date = self.cleaned_data['date']
        if not (time(8, 0) <= hour <= time(20, 0)):
            raise ValidationError("La hora debe estar entre las 8am y las 8pm.")
    
        now = datetime.now()

        # Combina la fecha y la hora para verificar si están en el pasado
        offer_datetime = datetime.combine(date, hour)
        if offer_datetime < now:
            raise ValidationError("La fecha y hora no pueden ser en el pasado.")

        return hour

        
class cashRegisterForm(forms.Form):
    cash = forms.CharField(label = 'Importe', widget=forms.TextInput())
    name = forms.CharField(label = 'Nombre del donante', widget=forms.TextInput())
    surname = forms.CharField(label = 'Apellido del donante', widget=forms.TextInput())
    dniDonor = forms.CharField(label = 'DNI del donante', widget=forms.TextInput())

class ComentPublicationForm(forms.Form):
    text = forms.CharField(label = 'Texto', widget=forms.TextInput(), max_length=255)

class articleRegisterForm(forms.Form):
    article = forms.CharField(label = 'Articulo', widget=forms.TextInput())
    category = forms.ChoiceField(label='Categoria', choices=[
        ('Alimento', 'alimento'),
        ('Electrodomestico', 'electrodomestico'),
        ('Limpieza', 'limpieza'),
        ('Higiene', 'higiene'),
        ('Juguete', 'juguete')
    ], widget=forms.Select())
    name = forms.CharField(label = 'Nombre del donante', widget=forms.TextInput())
    surname = forms.CharField(label = 'Apellido del donante', widget=forms.TextInput())
    dniDonor = forms.CharField(label = 'DNI del donante', widget=forms.TextInput())
        
class calificationForm(forms.Form):
    calification = forms.ChoiceField(label= 'Calificacion', choices=[
        (1 , '⭐'),
        (2,  '⭐⭐'),
        (3,  '⭐⭐⭐'),
        (4,  '⭐⭐⭐⭐'),
        (5,  '⭐⭐⭐⭐⭐'),
        ],
        widget=forms.RadioSelect,
    )