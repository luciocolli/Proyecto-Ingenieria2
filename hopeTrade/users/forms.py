from django import forms


class CreateNewUser(forms.Form):
    dni = forms.IntegerField(label="Dni", max_value=99999999, widget=forms.TextInput())
    name = forms.CharField(label="Nombre", max_length=100, widget=forms.TextInput())
    surname = forms.CharField(label="Apellido", max_length=100, widget=forms.TextInput())
    mail = forms.CharField(label="Mail", max_length=100, widget=forms.TextInput())
    date = forms.DateField(label="Fecha", widget=forms.TextInput(attrs={'type': 'date'}))
    password = forms.CharField(label="Contraseña", max_length=100, widget=forms.TextInput())



class CreatelogIn(forms.Form) :
    dni = forms.IntegerField(label="Dni", max_value=9999999, widget = forms.TextInput())
    password = forms.CharField(label="Contraseña", max_length=100, widget=forms.TextInput())