from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,AllowAny
import json
User = get_user_model()

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 允许任何用户访问此接口

    def post(self, request, *args, **kwargs):
        try:
            raw_json = next(iter(request.POST.keys()))
            data = json.loads(raw_json)
        except (StopIteration, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': str(user.id),
            'email': str(user.email),
        })


class SigninView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 允许任何用户访问此接口

    def post(self, request, *args, **kwargs):
        try:
            raw_json = next(iter(request.POST.keys()))
            data = json.loads(raw_json)
        except (StopIteration, json.JSONDecodeError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        try:
            user = User.objects.get(email=data.get("email"))
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(data.get("password")):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })



class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'id': request.user.id,
            'email': request.user.email,
        })