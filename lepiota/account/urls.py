from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from .views import UserDetails, GroupList, SignUp


app_name = 'account'


# User endpoints
urlpatterns = [
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]


# Custom sign-up form
urlpatterns += [

    path(
        'signup/', 
        SignUp.as_view(), 
        name='signup'
    ),
]


# Default django auth views
urlpatterns += [

    path(
        'change-password/', 
        auth_views.PasswordChangeView.as_view(), 
        name="password_change_form"
    ),
    
    path(
        'change-password/done/', 
        auth_views.PasswordChangeDoneView.as_view(), 
        name="password_change_done"
    ),
    
    path(
        'reset-password/', 
        auth_views.PasswordResetView.as_view(), 
        name="password_reset"
    ),
    
    path(
        'reset-password/done/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name="password_reset_done"
    ),
    
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"
    ),
    
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(), 
        name="password_reset_complete"
    ),
]
