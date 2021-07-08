from django.urls import path
from . import views

app_name = 'rest_api'

urlpatterns = [
    path('', views.TestView.as_view()),
    path('<int:id><str:title>', views.TestView.as_view()),
]
