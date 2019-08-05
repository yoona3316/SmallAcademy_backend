from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='user_signup'),
    path('', include('rest_auth.urls')),
    path('active/<str:uidb64>/<str:token>/', views.UserActivate.as_view(), name='user_activate'),
]
