from django import forms
from .models import Publication
from hopeTrade.settings import STATIC_URL, BASE_DIR
import os


def get_png_files():
    static_dir = os.path.join(BASE_DIR, "landing",STATIC_URL)
    png_files = [f for f in os.listdir(static_dir) if f.endswith('.png')]
    return [(f, f) for f in png_files]

class CreateNewPublication(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, widget=forms.TextInput())
    description = forms.CharField(label='Descripcion', max_length=500, widget=forms.TextInput())
    category = forms.ChoiceField(label='Categoria', choices=[('alimento', 'Alimento'), ('limpieza', 'Limpieza'), ('higiene', 'Higiene'), ('electrodomestico', 'Electrodomestico'), ('jueguete', 'Juguetes')], widget=forms.Select())
    #category = forms.CharField(label='Categoria', max_length=100, widget=forms.TextInput())
    state = forms.ChoiceField(label='Estado del Producto', choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')], widget=forms.Select())
    date = forms.DateField(label='Fecha de Vencimiento', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    file = forms.ChoiceField(label= 'Nombre del archivo png', choices= get_png_files(), required=False)

    
class EditPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ['user', 'file']
        widgets = {
            'category': forms.Select(choices=[('alimento', 'Alimento'), ('limpieza', 'Limpieza'), ('higiene', 'Higiene'), ('electrodomestico', 'Electrodomestico'), ('jueguete', 'Juguetes')]),
            'state': forms.Select(choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')]),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class cashRegisterForm(forms.Form):
    cash = forms.CharField(label = 'Importe', widget=forms.TextInput())
    name = forms.CharField(label = 'Nombre del donante', widget=forms.TextInput())
    surname = forms.CharField(label = 'Apellido del donante', widget=forms.TextInput())
    dniDonor = forms.CharField(label = 'DNI del donante', widget=forms.TextInput())

class ComentPublicationForm(forms.Form):
    text = forms.CharField(label = 'Texto', widget=forms.TextInput(), max_length=255)
        