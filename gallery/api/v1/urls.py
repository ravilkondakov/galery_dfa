from django.urls import path

from api.v1.views.auth import AuthWithEmailView

urlpatterns = [
    path('auth/', AuthWithEmailView.as_view(), name='auth'),
]
