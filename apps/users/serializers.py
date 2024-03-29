from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User
from rest_framework import serializers


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Email or password is incorrect')
                raise serializers.ValidationError(detail=msg)
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(detail=msg)
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'photo',
        ]
