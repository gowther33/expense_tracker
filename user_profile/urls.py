from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('profile/',views.profile_admin,name="admin_profile"),
    path('profile_user/',views.profile_user,name="user_profile"),
    path('change-password/',views.change_password,name="password_change"),
    path('change-email-pref',views.change_email_pref,name="change_email_pref"),
    path('change-email-pref-user',views.change_email_pref_user,name="change_email_pref_user")
]
