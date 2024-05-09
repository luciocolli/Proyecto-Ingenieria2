from django import forms
from .models import Publication

class CreateNewPublication(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, widget=forms.TextInput())
    description = forms.CharField(label='Descripcion', max_length=500, widget=forms.TextInput())
    category = forms.CharField(label='Categoria', max_length=100, widget=forms.TextInput())
    state = forms.CharField(label='Estado del Producto', max_length=100, widget=forms.TextInput())
    date = forms.DateField(label='Fecha de Vencimiento', widget=forms.DateInput(attrs={'type': 'date'}) )
    
class EditPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ['user']

