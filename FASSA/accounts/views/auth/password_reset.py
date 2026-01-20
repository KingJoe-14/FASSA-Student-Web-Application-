from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from ...models import PasswordResetOTP, User
from ...serializers.auth.password_reset import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from ...utils import send_password_reset_otp

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "If this account exists, a code was sent."}, status=200)

        PasswordResetOTP.objects.filter(email=email).delete()

        otp = PasswordResetOTP.generate_otp()
        PasswordResetOTP.objects.create(email=email, otp=otp)

        send_password_reset_otp(email, otp)
        return Response({"detail": "Check your email for the code."}, status=200)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        reset_obj = get_object_or_404(PasswordResetOTP, email=email, otp=otp)

        user = User.objects.get(email=email)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        reset_obj.delete()

        return Response({"detail": "Password reset successful."})
