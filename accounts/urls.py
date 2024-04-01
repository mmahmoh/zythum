from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns: list = [
    path(
        'login/',
        views.LoginFormView.as_view(),
        name='login'
    ),
    path(
        'signup/',
        views.SignupFormView.as_view(),
        name='signup'
    ),
    path(
        'activate/<uidb64>/<token>/',
        views.SignUpActivation.as_view(),
        name='activate_account',
    ),
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile',
    ),
    path(
        'logout/',
        views.LogoutUserView.as_view(),
        name='logout',
    ),
]
