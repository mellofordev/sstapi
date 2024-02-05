
from django.urls import path,include
from .views import *
urlpatterns = [
    path('programs/<slug:slug>',programs_api),
    path('departmentpoints/',department_api),
    path('register/<slug:slug>/',program_register_api)
]
