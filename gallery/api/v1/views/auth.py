import datetime

from django.contrib.auth import get_user_model
from rest_framework import generics, status

from api.v1.serializers.auth import UserAuthSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

User = get_user_model()


class AuthWithEmailView(generics.CreateAPIView):
    serializer_class = UserAuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        password = request.data['password']
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            user = User.objects.create_user(phone=phone, password=password)
            user.is_active = True
            user.last_login = datetime.datetime.now()
            return Response('ok', status=status.HTTP_200_OK)
        else:
            return Response('Phone number is not valid', status=status.HTTP_400_BAD_REQUEST)
