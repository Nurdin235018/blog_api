from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Account successfully created', status=201)


class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response(
            'Account successfully activated', status=200
        )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('You successfully log outed from your account')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(
            'Password successfully installed', status=200
        )


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_verification_email()
        return Response('We sent you a message to reinstall your password')


class ForgotConfirmPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password successfully reinstalled')

