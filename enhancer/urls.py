from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('upload/', views.upload_image, name='upload_image'),
    path("success/", views.success_page, name="success"),
]
