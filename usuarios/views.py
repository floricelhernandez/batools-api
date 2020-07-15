from django.forms import Form
from django.shortcuts import render
from django.views import generic
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from usuarios.models import *
from django.conf import settings
from django import forms
# Create your views here.


class CustomLoginForm(Form):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomSignupForm(Form):
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
