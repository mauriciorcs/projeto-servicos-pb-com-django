from django.urls import path
from .views import MapView

urlpatterns = [
    path('map/', MapView.as_view(), name='map'),  # Rota para sua view
]
