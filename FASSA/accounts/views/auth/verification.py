from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ...models import AccountVerificationOTP, User
from ...utils import send_verification_otp

class VerifyStudentAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=400)

        record = AccountVerificationOTP.objects.filter(email=email, otp=otp).first()
        if not record:
            return Response({"error": "Invalid or expired OTP."}, status=400)

        if record.is_expired():
            record.delete()
            return Response({"error": "OTP expired."}, status=400)

        user = get_object_or_404(User, email=email)
        user.is_verified = True
        user.is_active = True
        user.save()

        record.delete()
        return Response({"message": "Account verified successfully."})

#resend verification
class ResendVerificationOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=400)

        user = get_object_or_404(User, email=email)

        if user.is_verified:
            return Response({"message": "Already verified."}, status=400)

        last_otp = AccountVerificationOTP.objects.filter(email=email).order_by('-created_at').first()

        if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 60:
            return Response({"error": "Wait before requesting a new OTP."}, status=429)

        AccountVerificationOTP.objects.filter(email=email).delete()

        otp_code = AccountVerificationOTP.generate_otp()
        AccountVerificationOTP.objects.create(email=email, otp=otp_code)

        send_verification_otp(email, otp_code)
        return Response({"message": "Verification code sent."})
