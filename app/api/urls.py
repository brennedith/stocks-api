from django.urls import path

from api.logic.integrator_factory import IntegratorFactory
from api.logic.sources.wallstreetsurvivor_source import WallStreeSurvivorSource

app_name = 'api'

urlpatterns = [
    path('wallstreetsurvivor', IntegratorFactory(WallStreeSurvivorSource), name='wallstreetsurvivor'),
]