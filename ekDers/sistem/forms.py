from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .widgets import BootstrapDateTimePickerInput
from .models import *
from .choices import BOLUM_CHOICES
from django.core.validators import FileExtensionValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Sicil No')
    password = forms.CharField(max_length=100, label='Parola', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Sicil Numarısını veya Parolayı Yanlış Girdiniz')
            return super(LoginForm, self).clean()

            
class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].label = 'Sicil No'

    email = forms.EmailField()
    Fakulte = forms.CharField()
    Bolum = forms.ChoiceField(choices=BOLUM_CHOICES)
    Dersyuku = forms.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        fields_required = ['first_name', 'last_name']
        help_texts = {
        'username': 'Sicil Numaranızı Giriniz.',
        }


class UploadForm(forms.Form):

    tarih1 = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=BootstrapDateTimePickerInput(),
        label='Başlangıç Tarihi'
    )

    tarih2 = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=BootstrapDateTimePickerInput(),
        label='Bitiş Tarihi'
    )

    excelUpload = forms.FileField(label='Excel Dosyası')



class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].label = 'Sicil No'

    email = forms.EmailField()
    
    class Meta:
        model = User
        fields =  ['username','first_name', 'last_name', 'email']
        fields_required = ['first_name', 'last_name']
        help_texts = {
            'username': 'Sicil Numaranızı Giriniz.' ,
        }

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile        
        fields = ['bolum', 'fakulte', 'dersYuku']

class AdminUploadForm(forms.Form):
    bas_satir = forms.IntegerField(label='Başlangıç Satırı:')
    son_satir = forms.IntegerField(label='Son Satır:')
    excel = forms.FileField(label='Excel :')

class DersForm(forms.ModelForm):
    class Meta:
        model = Dersler
        fields = ['dersAdı','dersKodu','dersKredisi', 'ikinciOgretim']