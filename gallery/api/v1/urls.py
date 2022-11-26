from django.urls import path

from api.v1.views.auth import AuthWithEmailView

from api.v1.views.gallery import ListImageView, CreateImageView, DeleteImageView

from api.v1.views.gallery import GetCurrentUserView

"""AUTH"""
urlpatterns = [
    path('auth/', AuthWithEmailView.as_view(), name='auth'),
]

"""GALLERY"""
urlpatterns += [
    path('gallery/', ListImageView.as_view(), name='gallery_view'),
    path('create_image/', CreateImageView.as_view(), name='create_image_view'),
    path('delete_all_images/', DeleteImageView.as_view(), name='delete_images_view'),
]

"""USER"""

urlpatterns += [
    path('user/', GetCurrentUserView.as_view(), name='get_current_user')
]
