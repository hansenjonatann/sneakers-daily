from django.urls import path 
from . import views

urlpatterns = [
  path('' , views.index , name='index'),
  path('test-connection/' , views.connection_test , name='test-connection'),
  path('predict/' , views.predictView , name='predictView'),
  path('predictprocess/' , views.predict , name='predictprocess')
]