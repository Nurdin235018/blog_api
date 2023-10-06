from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_code
from django.core.mail import send_mail


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=5, required=True)
    password_confirm = serializers.CharField(min_length=5, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exist')
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_code(user.email, user.activation_code)
        return user


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                'Password doesn\'t match'
            )
        return attrs


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User didn\'t found')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User is not found'
            )
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(username=email, password=password, request=request)
        print('==================')
        print(user)
        print('==================')
        if not user:
            raise serializers.ValidationError(
                'Email or Password is wrong'
            )
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=5, required=True)

    def validate_password(self, password):
        user = self.context.get('request').user
        if not user.check_password(password):
            raise serializers.ValidationError(
                'Password is wrong'
            )
        return password

    def set_new_password(self):
        user = self.context.get('request').user
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User is not found'
            )
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            "Reset the password",
            f'Your code: {user.activation_code}',
            'test@gmail.com',
            [user.email]
        )

class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=5, required=True)
    new_password_confirm = serializers.CharField(min_length=5, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        pass1 = attrs.get('new_password')
        pass2 = attrs.get('new_password_confirm')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValueError(
                'User is not found'
            )
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords dont match')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('new_password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()




