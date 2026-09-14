from django.urls import path
from .views import SignUpView, MeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('me/', MeView.as_view(), name='me'),
]