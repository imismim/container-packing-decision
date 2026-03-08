from django.urls import path
from . import views
urlpatterns = [
    path('', views.start_page, name='start-page'),
    path('<slug:slug>/', views.index, name='variant')
]
