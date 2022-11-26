from rest_framework import generics, permissions, status

from apps.gallery.models import Gallery

from api.v1.serializers.gallery import GallerySerializer
from rest_framework.response import Response

from api.v1.serializers.user import UserSerializer
from apps.user.models import User


class ListImageView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


class CreateImageView(generics.CreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (permissions.IsAuthenticated,)


class DeleteImageView(generics.DestroyAPIView):
    queryset = Gallery.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetCurrentUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id)
        return user
