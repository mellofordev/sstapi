
from django.urls import path,include
from .views import *
urlpatterns = [
    path('programs/<slug:slug>',programs_api),
    path('departmentpoints/',department_api),
    path('register/<slug:slug>/',program_register_api),
    path('team/create/<slug:slug>/',create_team),
    path('team/join/<slug:slug>/',join_team),
    path("team/members/<slug:slug>/",get_team_members_api),
    path('program/delete/<slug:slug>/',delete_program_api)
]
