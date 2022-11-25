from django.contrib.gis.db import models

from apps.user.models import User


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_gallery')
    image = models.ImageField(upload_to='images/gallery')

    class Meta:
        verbose_name = "Галлерея"
        verbose_name_plural = "Галлереи"

    @property
    def gallery_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
