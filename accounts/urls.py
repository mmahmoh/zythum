from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns: list = [
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('signup/', views.SignupFormView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.SignUpActivation.as_view(), name='activate-account'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('password/reset/', views.PasswordReset.as_view(), name='password-reset'),
    path('password/reset/done/', views.PasswordResetDone.as_view(), name='password-reset-done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmation.as_view(), name='password-reset-confirmation'),
    path('password/reset/complete/', views.PasswordResetComplete.as_view(), name='password-reset-complete'),
    path('password/change/', views.PasswordChange.as_view(), name='password-change'),
    path('profile/update/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('profile/delete/', views.ProfileDelete.as_view(), name='profile-delete'),

]
