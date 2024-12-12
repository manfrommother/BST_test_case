from django.urls import path
from .views import RobotCreateView, RobotExcelReportView


urlpatterns = [
    path('report/download/', RobotExcelReportView.as_view(), name='robot-report'),
    path('robots/api/', RobotCreateView.as_view(), name='robot-create'),
]