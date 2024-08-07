from django import forms
#from .models import User
#from . import backend as back

class CreateNewUser(forms.Form):
    dni = forms.IntegerField(label="Dni", max_value=99999999, widget=forms.TextInput(), error_messages={'invalid'  : 'Este campo debe contenter solo números',
                                                                                                        'max_value': 'El DNI ingresado no existe.'})
    name = forms.CharField(label="Nombre", max_length=100, widget=forms.TextInput())
    surname = forms.CharField(label="Apellido", max_length=100, widget=forms.TextInput())
    mail = forms.EmailField(label="Mail", max_length=100, widget=forms.EmailInput())
    date = forms.DateField(label="Fecha", widget=forms.TextInput(attrs={'type': 'date'}))
    password = forms.CharField(label="Contraseña", max_length=100, widget=forms.PasswordInput())



class CreatelogIn(forms.Form) :
    dni = forms.IntegerField(label="Dni", max_value=99999999, widget = forms.TextInput(), error_messages={'invalid': 'Este campo debe contenter solo números',
                                                                                                         'max_value': 'El DNI ingresado no existe.'})
    password = forms.CharField(label="Contraseña", max_length=100, widget=forms.PasswordInput())

class AddCard(forms.Form):
    number = forms.CharField(label= 'Número de tarjeta',
                             widget=forms.TextInput(),
                             max_length=18, 
                             min_length=13,
                             error_messages={
                                            'max_length': 'El número de la tarjeta no puede tener más de 18 caracteres.',
                                            'min_length': 'El número de la tarjeta debe tener al menos 13 caracteres.',
                                            'required': 'Este campo es obligatorio.',
                                            'invalid': 'Ingrese un número de tarjeta válido.'
                            })
 

class TransferDonation(forms.Form):
    number = forms.CharField(label= 'Número de tarjeta',
                             widget=forms.TextInput(),
                             max_length=18, 
                             min_length=13,
                             error_messages={
                                            'max_length': 'El número de la tarjeta no puede tener más de 18 caracteres.',
                                            'min_length': 'El número de la tarjeta debe tener al menos 13 caracteres.',
                                            'required': 'Este campo es obligatorio.',
                                            'invalid': 'Ingrese un número de tarjeta válido.'
                            })
    amount = forms.IntegerField(label = 'Monto en pesos',required= True, error_messages={'invalid' : 'Este campo debe contenter solo números'})
 

'''
class EditProfileForm(forms.ModelForm):
    password_actual = forms.CharField(widget=forms.PasswordInput, required=False)
    nueva_password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'date', 'mail']

    def clean(self):
        cleaned_data = super().clean()
        password_actual = cleaned_data.get('password_actual')
        nueva_password = cleaned_data.get('nueva_password')

        anios = cleaned_data.get('date')


        #Si saco este chequeo se rompe la pagina
        if anios is None:
            raise forms.ValidationError('La fecha de nacimiento es requerida.')

        #Chequeo 18 anios
        
        if back.get_years(anios) < 18:
            raise forms.ValidationError('Debes ser mayor de 18 años para modificar tu perfil.')

        # Verificar si tanto la contraseña actual como la nueva contraseña están en blanco
        if not password_actual and not nueva_password:
            return cleaned_data

        if (password_actual and not nueva_password) or (nueva_password and not password_actual):
            raise forms.ValidationError('Se deben proporcionar la contraseña actual y la nueva contraseña.')

        return cleaned_data
'''