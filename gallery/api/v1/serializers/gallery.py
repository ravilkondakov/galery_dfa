from rest_framework import serializers

from apps.gallery.models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    gallery_url = serializers.ImageField(
        use_url=True,
        source='image',
    )

    class Meta:
        model = Gallery
        fields = (
            'user', 'gallery_url'
        )

        read_only_fields = ('user',)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            user = request.user
            image = validated_data.get('image')
            gallery = Gallery(user=user, image=image)
            gallery.save()
            return gallery
