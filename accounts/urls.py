from django.urls import path

from . import views as accounts_views
from rest_framework.authtoken import views
urlpatterns = [
    path('api/signup/',accounts_views.signup_view,name='signupapi'),
    path('api/login/',views.obtain_auth_token),
    path('api/client/signup',accounts_views.client_signup),
    path('api/profile/',accounts_views.profile_api),
    path('api/profile/update/<slug:slug>',accounts_views.profile_department_set_api),
    path('export/profile',accounts_views.export_data),
    path('export/team',accounts_views.export_team_data),
    path('export/program',accounts_views.export_program_data),
    path('export/program/team',accounts_views.export_team_program_data)
]