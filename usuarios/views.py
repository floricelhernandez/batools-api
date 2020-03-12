from django.shortcuts import render
from django.views import generic
from usuarios.models import *
from allauth.account.forms import SignupForm, LoginForm
from django.conf import settings
from django import forms
# Create your views here.


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            print (fieldname)
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        perfil = Perfil()
        perfil.usuario = user
        digito = user.id
        ultimo_digito= digito % 10
        perfil.avatar = 'avatares/' + str(ultimo_digito) + '.png'
        perfil.save()
        return user

class LoginView(generic.View):

    def get(self, request):
        return render(request, 'usuarios/pages-login.html')
