from django.urls import path
from .views import home, warning, daily

urlpatterns = [
    path('real-time-chart', home, name="Realtime-Chart-App"),
    path('daily-chart', daily, name="Daily-Chart"),
    path('', warning, name="Warning")

]