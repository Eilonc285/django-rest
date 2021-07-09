from django.urls import path
from . import views

app_name = 'rest_api'

urlpatterns = [
    path('', views.BusinessView.as_view()),
    path('<int:id><str:title>', views.BusinessView.as_view()),
    path('webscraper', views.WebScraperView.as_view()),
]
