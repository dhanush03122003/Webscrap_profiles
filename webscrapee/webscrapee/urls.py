from django.urls import path
from webscrap_app import views
urlpatterns = [
    path('competetive_coding/',views.get_code_chef_det),
]
