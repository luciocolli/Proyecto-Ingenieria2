from django import forms
from .models import Card
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
class DeleteCard(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(DeleteCard, self).__init__(*args, **kwargs)
        self.user = user


        try:
            cards= Card.objects.filter(user=self.user.id)
            cards_numbers = [(card.id, card.number) for card in cards]
        except:
            cards_numbers = [('', 'Aquí aparecerán sus tarjetas cargadas')]
        
        # Definir el campo de elección con las tarjetas filtradas
        self.fields['card'] = forms.ChoiceField(label='Tarjetas', choices=cards_numbers)

    def get_user(self):
        print(self.user)
        return self.user