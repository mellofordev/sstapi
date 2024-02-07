from django.urls import path

from . import views as accounts_views
from rest_framework.authtoken import views
urlpatterns = [
    path('api/signup/',accounts_views.signup_view,name='signupapi'),
    path('api/login/',views.obtain_auth_token),
    path('api/client/signup',accounts_views.client_signup),
    path('api/profile/',accounts_views.profile_api),
    path('api/profile/update/<slug:slug>',accounts_views.profile_department_set_api)
]