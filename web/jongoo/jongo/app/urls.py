from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('login/', views.RegistrationLoginView.as_view(), name='login'),
    path('list/', views.post_list,name="post_list"),
    path('<slug:post>/', views.post_detail,name="post_detail"),
]