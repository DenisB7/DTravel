from django.urls import path

from app_travel.views import MainView
from app_travel.views import DepartureView
from app_travel.views import TourView
from app_travel.views import custom_handler404
from app_travel.views import custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('departure/<str:departure>/', DepartureView.as_view(), name='departure'),
    path('tour/<int:tour_id>/', TourView.as_view(), name='tour'),
]
