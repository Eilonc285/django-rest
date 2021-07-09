from django.urls import path
from . import views

app_name = 'rest_api'

urlpatterns = [
    path('', views.BusinessView.as_view(), name='get_all'),
    path('<int:id><str:title>', views.BusinessView.as_view(), name='get_one'),
    path('webscraper', views.WebScraperView.as_view(), name='web_scraper'),
]
