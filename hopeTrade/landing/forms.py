from django import forms
from .models import Publication

class CreateNewPublication(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, widget=forms.TextInput())
    description = forms.CharField(label='Descripcion', max_length=500, widget=forms.TextInput())
    category = forms.ChoiceField(label='Categoria', choices=[('alimento', 'Alimento'), ('limpieza', 'Limpieza'), ('higiene', 'Higiene'), ('electrodomestico', 'Electrodomestico'), ('jueguete', 'Juguetes')], widget=forms.Select())
    #category = forms.CharField(label='Categoria', max_length=100, widget=forms.TextInput())
    state = forms.ChoiceField(label='Estado del Producto', choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')], widget=forms.TextInput())
    date = forms.DateField(label='Fecha de Vencimiento', widget=forms.DateInput(attrs={'type': 'date'}) )
    file = forms.CharField(label= 'Nombre del archivo png', max_length=100, widget=forms.TextInput())
    
class EditPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ['user', 'file']
        