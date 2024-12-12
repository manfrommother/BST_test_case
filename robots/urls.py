from django.urls import path
from .views import RobotCreateView

urlpatterns = [
    path('api/robots/', RobotCreateView.as_view(), name='robot-create'),
]