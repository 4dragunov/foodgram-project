from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("change_user_password/", auth_views.PasswordChangeView.
         as_view(template_name='registration/change_user_password.html',
                 success_url=reverse_lazy('change_user_password_done')),
         name="change_user_password"),
    path("change_user_password/done/", auth_views.PasswordChangeDoneView.
         as_view(template_name='registration/change_user_password_done.html'),
         name="change_user_password_done"),
    path("password-reset/", auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path("password-reset/complete/",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("user_logout/", auth_views.LogoutView.as_view(
        template_name='registration/logout.html'), name="user_logout"),

]
