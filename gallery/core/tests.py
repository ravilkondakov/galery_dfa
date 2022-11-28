from django.test import TestCase

from apps.gallery.models import Gallery

from django.core.files.uploadedfile import SimpleUploadedFile

from apps.user.models import User

from api.v1.serializers.gallery import GallerySerializer


class SuccessGalleryTestCase(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(phone='+79888888888', password='test')
        user_2 = User.objects.create_user(phone='+79888888882', password='test_2')
        user_3 = User.objects.create_superuser(phone='+79888888884', password='test')
        Gallery.objects.create(user=user_1, image='images/gallery/6K7A0017.jpg')
        Gallery.objects.create(user=user_1, image='images/gallery/6K7A0017.jpg')
        Gallery.objects.create(user=user_2, image='images/gallery/6K7A0017.jpg')
        Gallery.objects.create(user=user_3, image='images/gallery/6K11A0017.jpg')

    def test_gallery_create_image(self):
        gallery_image = Gallery()
        gallery_image.image = SimpleUploadedFile(name='test.jpg',
                                                 content=open('static/images/images/gallery/test.jpg', 'rb').read(),
                                                 content_type='image/jpeg')
        user = User.objects.get(id=1)
        gallery_image.user = user
        gallery_image.save()
        self.assertEqual(Gallery.objects.count(), 5)

    def test_gallery_create_image_from_url(self):
        self.client.login(phone='+79888888888', password='test')
        user = User.objects.get(id=6)

        form_data = {
            'user': user,
            'gallery_url': '/images/gallery/test.jpg'
        }
        gallery_image = Gallery()
        num_of_gallery = Gallery.objects.all().count()
        self.assertEqual(num_of_gallery, 4)

        gallery_image.image = SimpleUploadedFile(name='test.jpg',
                                                 content=open(f'static/images/images/gallery/test.jpg',
                                                              'rb').read(),
                                                 content_type='image/jpeg')

        response = self.client.post('/api/v1/create_image/',
                                    data={
                                        'gallery_url': gallery_image.image
                                    })
        gallery = Gallery.objects.filter(user=form_data['user']).first()
        num_of_gallery = Gallery.objects.all().count()
        self.assertEqual(gallery.user, user)
        self.assertEqual(num_of_gallery, 5)
        self.assertEqual(response.status_code, 201)

    def test_gallery_get_all(self):
        self.client.login(phone='+79888888888', password='test')
        response = self.client.get('/api/v1/gallery/')
        response_count = response.content.decode("utf-8").count('}')
        data_count = Gallery.objects.all().count()
        self.assertEqual(response_count, data_count)

    def test_delete_all_gallery(self):
        self.client.login(phone='+79888888884', password='test')
        response = self.client.delete('/api/v1/delete_all_images/')
        data_count = Gallery.objects.all().count()
        self.assertEqual(0, data_count)
        self.assertEqual(response.status_code, 204)


class UnSuccessGalleryTestCase(TestCase):
    def setUp(self):
        user_2 = User.objects.create_user(phone='+79888888882', password='test_2')
        user_3 = User.objects.create_superuser(phone='+79888888884', password='test')
        Gallery.objects.create(user=user_2, image='images/gallery/6K7A0017.jpg')
        Gallery.objects.create(user=user_3, image='images/gallery/6K11A0017.jpg')

    def test_bad_delete_all_gallery(self):
        self.client.login(phone='+79888888882', password='test_2')
        response = self.client.delete('/api/v1/delete_all_images/')
        data_count = Gallery.objects.all().count()
        self.assertFalse(0, data_count)
        self.assertEqual(response.status_code, 403)


    def test_bad_gallery_create_image_from_url(self):
        self.client.login(phone='+79888888888', password='test')
        user = User.objects.get(id=3)

        form_data = {
            'user': 3,
            'gallery_url': '/images/gallery/test.jpg'
        }
        gallery_image = Gallery()
        num_of_gallery = Gallery.objects.all().count()
        self.assertEqual(num_of_gallery, 2)

        gallery_image.image = SimpleUploadedFile(name='test.jpg',
                                                 content=open(f'static/images/images/gallery/test.jpg',
                                                              'rb').read(),
                                                 content_type='image/jpeg')

        response = self.client.post('/api/v1/create_image/',
                                    data={
                                        'gallery_url': ''
                                    })
        gallery = Gallery.objects.filter(user=form_data['user']).first()
        num_of_gallery = Gallery.objects.all().count()
        self.assertEqual(gallery.user, user)
        self.assertEqual(num_of_gallery, 2)
        self.assertEqual(response.status_code, 401)
