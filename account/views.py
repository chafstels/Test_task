from rest_framework.viewsets import ModelViewSet
from .serializers import RegistrationSerializer, ActivationSerializer, UserSerializer, ResetPasswordSerializer, \
    ConfirmPasswordSerializer, LogoutSerializer
from rest_framework.generics import GenericAPIView, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .task import send_connfirmation_email_task, send_confirmation_password_task
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class RegistrationView(GenericAPIView):
    permission_classes = permissions.AllowAny,
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_connfirmation_email_task.delay(user.email, user.activation_code)
            except:
                return Response({'message': "Registered, but the code was not sent to the email.",
                                 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class ActivationView(GenericAPIView):
    permission_classes = permissions.AllowAny,
    serializer_class = ActivationSerializer

    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activated.', status=200)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully activated.', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.IsAdminUser,


class LogoutView(GenericAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(GenericAPIView):
    permission_classes = permissions.AllowAny,
    serializer_class = ConfirmPasswordSerializer
    def get(self, request):
        return Response({'message': 'Please provide an email to reset the password.'})

    def post(self, request):
        serializer = ConfirmPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                user.create_activation_code()
                user.save()
                send_confirmation_password_task.delay(user.email, user.activation_code)
                return Response({'activation_code': user.activation_code}, status=200)
            except ObjectDoesNotExist:
                return Response({'message': 'User with this email does not exist.'}, status=404)
        return Response(serializer.errors, status=400)


class ResetPasswordConfirmView(GenericAPIView):
    permission_classes = permissions.AllowAny,
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.activation_code = ''
        user.save()
        return Response('Your password has been successfully updated.', status=200)


class UserProfileVIEW(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        profile = get_object_or_404(User, email=user.email)
        serializer = UserSerializer(instance=profile)
        return Response(serializer.data, status=200)

def auth_github(request):
    return render(request, 'oauth_github.html')