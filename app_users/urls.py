from django.urls import path
from app_users import views
from django.contrib.auth import views as auth_views

# app_name = 'app_users'
urlpatterns = [
    path('',views.HomeView.as_view(),name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('contact/', views.ContactView.as_view(), name="contact"),
    path('contact/',views.contact , name='contact'),

    path('change_password', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(),
    name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),

    path('profile',views.profile , name='profile'),
    path('profile/edit',views.profile_edit , name='profile_edit'),

]
